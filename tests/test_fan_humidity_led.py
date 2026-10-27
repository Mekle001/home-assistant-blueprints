"""Guard the handoff between a running preset and automatic humidity LEDs.

Run: python3 -m unittest discover -s tests
Requires PyYAML and Jinja2, used to parse HA input tags and render conditions.
"""
import json
from pathlib import Path
import unittest

import jinja2
import yaml

ROOT = Path(__file__).resolve().parents[1]

class Loader(yaml.SafeLoader):
    pass

Loader.add_constructor('!input', lambda loader, node: loader.construct_scalar(node))

class HumidityLedPriority(unittest.TestCase):
    def setUp(self):
        self.configs = [yaml.load((ROOT / 'automation' / f'inovelli_{kind}_fan_timer.yaml').read_text(), Loader=Loader)
                        for kind in ('blue', 'red')]

    def render(self, template, *, timer='idle', current=0, enabled=True, trigger='humidity_on', owned='off', hold='on', fan='on'):
        states = {'timer.preset': timer, 'input_boolean.led': owned,
                  'input_boolean.humidity': hold, 'light.fan': fan}
        env = jinja2.Environment(undefined=jinja2.StrictUndefined)
        env.filters['to_json'] = json.dumps
        env.globals['is_state'] = lambda entity, state: states.get(entity) == state
        result = env.from_string(template).render(
            trigger={'id': trigger}, this={'attributes': {'current': current}},
            humidity_enabled=enabled, automatic_hold='input_boolean.humidity',
            humidity_led_owned='input_boolean.led', fan_load='light.fan', timer='timer.preset',
            humidity_color=127, humidity_intensity=30)
        return result.strip() == 'True'

    def test_background_events_cannot_restart_a_preset_countdown(self):
        for config in self.configs:
            for trigger in ('humidity_on', 'humidity_off', 'humidity_reconcile', 'humidity_restore'):
                for timer, current in [('active', 1), ('paused', 0), ('idle', 1), ('unknown', 0), ('unavailable', 0)]:
                    with self.subTest(trigger=trigger, timer=timer, current=current):
                        self.assertFalse(self.render(config['condition'][0], trigger=trigger, timer=timer, current=current))
            self.assertTrue(self.render(config['condition'][0]))
            self.assertFalse(self.render(config['condition'][0], enabled=False))

    def test_paddle_and_timer_expiry_keep_their_priority(self):
        for config in self.configs:
            for trigger in ('paddle_up', 'paddle_down', 'timer_finished'):
                self.assertTrue(self.render(config['condition'][0], timer='active', current=1, trigger=trigger))
            self.assertFalse(config['blueprint']['input']['humidity_section']['input']['humidity_led_enabled']['default'])

    def test_humidity_status_never_operates_fan_or_preset_timer(self):
        def walk(value):
            if isinstance(value, dict):
                if 'service' in value:
                    yield value['service']
                for child in value.values():
                    yield from walk(child)
            elif isinstance(value, list):
                for child in value:
                    yield from walk(child)
        for config in self.configs:
            status = config['action'][0]['choose'][0]
            services = list(walk(status))
            self.assertTrue(services)
            self.assertFalse(any(s.startswith(('light.', 'fan.', 'homeassistant.', 'timer.')) for s in services))
            desired = status['sequence'][0]['choose'][0]['conditions'][0]
            self.assertTrue(self.render(desired))
            for kwargs in ({'hold': 'off'}, {'fan': 'off'}, {'fan': 'unavailable'}, {'timer': 'active'}):
                self.assertFalse(self.render(desired, **kwargs))

    def test_expiry_handoff_is_explicit_after_countdown_cleanup(self):
        for config in self.configs:
            finish = next(b for b in config['action'][0]['choose'] if b['conditions'] == "{{ trigger.id == 'timer_finished' }}")
            off = next(s for s in finish['sequence'] if 'automatic_hold' in str(s.get('if', '')))
            self.assertIn('else', off)
            self.assertIn('else', config['action'][-1])
            self.assertEqual(config['action'][1]['alias'], 'Yield the full bar before the preset countdown writes segments')

if __name__ == '__main__':
    unittest.main()
