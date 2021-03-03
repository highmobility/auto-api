# AutoAPI L13 Changelog

**Level 13** contains a single _minor_ change of the protocol with the _events_ types.  

Excluding the _events_ change, **L13** contains only additive updates to the protocol.  
Meaning there is no need to update generators and other tools built on the protocol's "architecture" (except for the minor _events_ change).

**These include**:  
- deprecations  
- new capabilities  
- new properties  
- new property field  
- new types  
- renamings  
- updates to enums  

Changes from L12 are divided into these sub-sections:
* [Capabilities](#capabilities)
* [Custom Types](#custom-types)
* [Enums](#enums)
* [Properties](#properties)
* [Misc](#misc)


## Capabilities

New capabilities, along with new properties (and their respective types), are introduced to the spec:

- _adas_
- *charging_session*
- _crash_


## Custom Types

The update brings a bunch of new (custom) types to the spec.  
Some are added to existing capabilities, while many come with _new_ capabilities.  

List of new _custom types_:

- `charging_cost`
- `crash_incident`
- `charging_location`
- `charging_point`
- `eco_driving_threshold`
- `engine_type`
- `lane_keep_assist_state`
- `lock_safety`
- `muted`
- `park_assist`
- `trip_meter`


## Enums

Some enums have gained new values.  
Besides `.brand`'s (universal property) change for a few names (for compiler/generator sanity), all the updates are additive.

List of updated enums (in custom types):

- `dashboard_lights.name` (a ton of new values)
- `failure.reason`
- `fluid_level`
- `location_wheel`


## Properties

New properties (along with some new _custom types_) are added to the pre-existing capabilities:

- *dashboard_lights*
  - `bulb_failures`
- _diagnostics_
  - `backup_battery_remaining_time`
  - `engine_coolant_fluid_level`
  - `engine_oil_amount`
  - `engine_oil_fluid_level`
  - `engine_oil_level`
  - `engine_oil_pressure_level`
  - `engine_time_to_next_service`
  - `engine_total_idle_operating_time`
  - `estimated_secondary_powertrain_range`
  - `fuel_level_accuracy`
  - `low_voltage_battery_charge_level`
  - `tire_pressures_targets`
  - `tire_pressures_differences`
- _engine_
  - `start_stop_enabled`
- _hood_
  - `lock`
  - `lock_safety`
- _lights_
  - `parking_light_status`
- _maintenance_
  - `distance_to_next_oil_service`
  - `time_to_next_oil_service`
- _trips_
  - `event`
  - `eco_level`
  - `maximum_speed`
  - `thresholds`
  - `total_fuel_consumption`
  - `total_idle_fuel_consumption`
- _trunk_
  - `lock_safety`
- _usage_
  - `trip_meters`
- *vehicle_information*
  - `powertrain_secondary`
- *vehicle_location*
  - `gps_signal_strength`
  - `gps_source`


## Misc

**New** type of reference in spec `events.[type]` which references a type from the file `misc/events.yml`.  
Currently the file contains only 1 type, so it would be referenced as `events.event` (in webhook custom type).

Other changes are:

- changed _engine_'s `activate_deactivate_start_stop` setter to `enable_disable_start_stop` (uses a new property too)
- new setter in `historical` called `get_charging_sessions`
  - only "entry point" for requesting `charging_session` data
- new property (optional) field `added: [version]`
  - indicates _AutoAPI Level_ (version) in which the property was introduced (added)
  - is only added to "newer" properties (latest levels)
- removed `diagnostics.blind_spot_monitoring` in favour of `adas` properties

*Deprecated* properties:

- _ignition_
  - `accessories_status` in favour of `state`
  - `status` in favour of `state`

