# Home Assistant Blueprints

## Inovelli Red VZW30 Fan Preset Timer

[![Open your Home Assistant instance and show the blueprint import dialog with this blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FMekle001%2Fhome-assistant-blueprints%2Fmain%2Fautomation%2Finovelli_red_fan_timer.yaml)

Import URL:

`https://raw.githubusercontent.com/Mekle001/home-assistant-blueprints/main/automation/inovelli_red_fan_timer.yaml`

Blueprint source:

`automation/inovelli_red_fan_timer.yaml`

This Z-Wave JS automation blueprint provides the same preset timer and
seven-segment countdown as the VZM30 version for the VZW30-SN Red On/Off
switch. Select the VZW30 device and a dedicated timer helper; the blueprint
listens for the device's Scene 001 and Scene 002 events and derives its native
load entity automatically. Leave the switch's built-in Advanced Timer Mode
disabled.

The countdown uses the VZW30's individual LED effect parameters 64, 69, 74,
79, 84, 89, and 94 through Z-Wave JS partial configuration writes. The
blueprint clears those same seven individual effects when the timer is
cancelled or expires, restoring the normal LED state.

Expired countdown segments remain under a solid notification at zero intensity
until final cleanup. Clearing or disabling an individual effect during the
countdown would reveal the switch's normal load-on color instead of leaving the
segment dark.

## Inovelli Blue VZM30 Fan Preset Timer

[![Open your Home Assistant instance and show the blueprint import dialog with this blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FMekle001%2Fhome-assistant-blueprints%2Fmain%2Fautomation%2Finovelli_blue_fan_timer.yaml)

Import URL:

`https://raw.githubusercontent.com/Mekle001/home-assistant-blueprints/main/automation/inovelli_blue_fan_timer.yaml`

Blueprint source:

`automation/inovelli_blue_fan_timer.yaml`

This Zigbee2MQTT automation blueprint replaces the VZM30-SN's built-in fan
timer. A paddle-up press starts at 5 minutes; each additional press advances
through 10, 15, and 30 minutes to a four-hour maximum run time. Paddle down
cancels the timer and turns the fan off. All durations are configurable.

The seven switch LEDs show proportional time remaining. Timer presets default
to green, cyan, yellow, orange, and violet; the final segment pulses red before
the fan turns off. The blueprint uses temporary LED effects, then clears them
so the switch returns to its normal LED configuration.

Create a dedicated Home Assistant timer helper for each fan before configuring
the blueprint. Select the VZM30 device and the timer helper; the blueprint
derives the switch's Zigbee2MQTT `light` load entity. Leave the switch's
built-in Fan Timer Mode disabled.
The blueprint normally calculates the switch topic as `zigbee2mqtt/<device
name>`; an optional full-topic override handles renamed devices or a custom
Zigbee2MQTT base topic.

Zigbee2MQTT exposes the VZM30-SN LED-effect composites to Home Assistant as
read-only sensors. The blueprint therefore uses Home Assistant entities for
button events, the load, and the timer, while publishing only the temporary
per-LED effect commands through Home Assistant's MQTT service.

## Light Preset Cycle From Select

[![Open your Home Assistant instance and show the blueprint import dialog with this blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FMekle001%2Fhome-assistant-blueprints%2Fmain%2Fautomation%2Flight_preset_cycle.yaml)

Import URL:

`https://raw.githubusercontent.com/Mekle001/home-assistant-blueprints/main/automation/light_preset_cycle.yaml`

Blueprint source:

`automation/light_preset_cycle.yaml`

For Inovelli switches, use the **Switches**, **Button**, and **Press type**
selectors. Those switches must also be selected in one running instance of
the **Inovelli — readable button events** decoder below. Legacy/custom triggers
remain available in the collapsed **Advanced triggers and conditions** section.
Avoid configuring both trigger paths for the same press, which would run twice.

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

Each option may end with an optional human-readable label after `#`. The label
is ignored when the preset is applied:

```text
ct|2700 # Soft white
ct|3500 # Neutral white
ct|5000 # Daylight
ct|6500 # Cool daylight
hs|0|100 # Red
fx|colorloop # Party mode
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
ct|2700 # Soft white
ct|3500 # Neutral white
ct|5000 # Daylight
ct|6500 # Cool daylight
hs|210|100 # Blue
hs|30|100 # Amber
hs|210|100|effect=colorloop # Blue color loop
rgb|255|0|128 # Magenta
rgb|255|0|128|brightness=180|effect=breathe # Magenta breathe
bri|64 # Dim
fx|colorloop # Party mode
fx|stop_colorloop # Stop party mode
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

## Appliance Group Displays

[Import blueprint](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FMekle001%2Fhome-assistant-blueprints%2Fmain%2Fautomation%2Fappliance_group_display.yaml)

Source: `automation/appliance_group_display.yaml`

Displays laundry or dishwasher status on one or several Inovelli Blue
Zigbee2MQTT switches, using a configurable LED script. Running loads pulse;
completed loads stay solid until acknowledged. Laundry uses cyan at the bottom
and orange at the top; dishwashers use magenta, with right at the bottom and
left at the top. Refrigerator warnings use the middle LEDs. Reserve each
switch for one display group. Completion tracking and phone notifications
remain separate automations.

Defaults include 60% daytime brightness, 10% during quiet hours with the switch
off, and 30% caps for cyan and magenta. Switches turned on during quiet hours
use the daytime levels. Targets and acknowledgement event entities are lists.

Requires the configured Inovelli Blue LED control script, pending-load helpers,
and appliance status entities. Minimum Home Assistant version: 2026.7.

## LG Laundry Pending Load

[Import blueprint](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2FMekle001%2Fhome-assistant-blueprints%2Fmain%2Fautomation%2Flg_laundry_pending_load.yaml)

Source: `automation/lg_laundry_pending_load.yaml`

Tracks a genuine running-to-end transition in an LG laundry status sensor and
latches an input_boolean until acknowledgement or a new cycle. Off, unavailable,
idle, and an initial end state do not imply completion. Use one instance per
appliance; LED displays and phone routing are separate. Minimum Home Assistant
version: 2024.10.

## Inovelli Readable Button Events

Source: `automation/inovelli_button_decoder.yaml`

One shared decoder instance accepts an array of MQTT action event entities and
emits `inovelli_button` events. Select each source in exactly one decoder.
Consumers can filter on `action: config_single`, `up_double`, or other supported
gestures and on `entity_id` to identify the source. Event data also includes
`button`, `press`, and `schema_version: 1`. The decoder reads the triggering
snapshot, accepts old combined and new split formats, and ignores unsupported
or restored events. It does not replay historical presses. Keep it enabled:
consumers using readable events depend on it. Minimum Home Assistant: 2026.7.

For a preset consumer, choose the switches, button, and press type directly in
Light Preset Cycle From Select. Existing custom-trigger instances continue to
work. Migration removes their old triggers and button conditions to prevent
double execution. Roll back a consumer by restoring its previous inputs; stop
the decoder only after all of its consumers have been rolled back.
