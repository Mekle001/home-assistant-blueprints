# Home Assistant Blueprints

## Light Preset Cycle From Select

[![Open your Home Assistant instance and show the blueprint import dialog with this blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2FMekle001%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Fautomation%2Flight_preset_cycle.yaml)

Import URL:

`https://github.com/Mekle001/home-assistant-blueprints/blob/main/automation/light_preset_cycle.yaml`

Blueprint source:

`automation/light_preset_cycle.yaml`

This automation blueprint cycles, resets, or reapplies light presets stored in a
hidden `input_select`. It is intended for smart bulbs or light groups where the
normal wall-switch behavior remains local/bound, while a scene/favorites button
chooses the bulb's rendered output: color temperature, static color, dynamic
color/effect, or brightness-only.

Preset format:

```text
ct|kelvin
ct|kelvin|brightness
ct|kelvin|effect=effect_name
ct|kelvin|brightness=brightness|effect=effect_name
hs|hue|saturation
hs|hue|saturation|brightness
hs|hue|saturation|effect=effect_name
hs|hue|saturation|brightness=brightness|effect=effect_name
rgb|red|green|blue
rgb|red|green|blue|brightness
rgb|red|green|blue|effect=effect_name
rgb|red|green|blue|brightness=brightness|effect=effect_name
bri|brightness
fx|effect_name
```

Brightness is optional for `ct`, `hs`, and `rgb` presets. Use either the old
positional form, such as `ct|2700|180`, or a named modifier, such as
`ct|2700|brightness=180`. When brightness is omitted, Home Assistant changes
only the color temperature or color and leaves the current brightness alone.
That is the preferred mode when wall dimmers are responsible for normal
brightness control.

Effects can be part of a color preset. For example, `hs|210|100|effect=colorloop`
sets a base color and starts the dynamic effect in one command. `fx` remains
available for effect-only commands such as stopping an effect. Only use effect
names exposed by the target light. Zigbee2MQTT lists ThirdReality bulb effects
such as `blink`, `breathe`, `okay`, `channel_change`, `finish_effect`,
`stop_effect`, `colorloop`, and `stop_colorloop`.

Example hidden helper options:

```text
ct|2700
ct|3500
ct|5000
hs|210|100
hs|30|100
hs|210|100|effect=colorloop
rgb|255|0|128
rgb|255|0|128|brightness=180|effect=breathe
bri|64
fx|colorloop
fx|stop_colorloop
```

Recommended gesture mapping:

- Favorites single press: `next`
- Favorites hold: `reset`, `previous`, `apply`, or `select`
- Paddle double press: `select` or `select_index` for a specific practical preset
- Avoid favorites double press; Inovelli uses that by default to clear switch notifications

For reset, put the normal/default preset first in the `input_select`. For
specific jumps, use either:

- `select`: enter the exact preset string, such as `ct|2700`, `ct|5000`, or
  `hs|210|100|effect=colorloop`
- `select_index`: enter the zero-based option index, where `0` is the first
  option in the `input_select`
