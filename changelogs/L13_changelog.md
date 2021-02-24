# AutoAPI L13 Changelog

**Level 13** contains a single _minor_ change of the protocol with the _events_ types.  

Excluding the _events_ change, **L13** contains only additive updates to the protocol.  
Meaning there is no need to update generators and other tools built on the protocol's "architecture" (except for the minor _events_ change).

**These include**:  
- deprecations  
- new capabilities  
- new properties  
- renamings  
- updates to enums  

Changes from L12 are divided into these sub-sections:
* [Capabilities](#capabilities)
* [Properties](#properties)
* [Misc](#misc)


## Capabilities

New capabilities, along with new properties (and their respective types), are introduced to the spec:

- _adas_
- *charging_session*
- _crash_


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
 - `tire_pressures_targets`
 - `tire_pressures_differences`
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
- *vehicle_location*
  - `gps_signal_strength`
  - `gps_source`


## Misc

**New** type of reference in spec `events.[type]` which references a type from the file `misc/events.yml`.  
Currently the file contains only 1 type, so it would be referenced as `events.event` (in webhook custom type).

Other changes are:

- additional `dashboard_lights` names (a lot of)
- additions to non-dashboard pre-existing _enums_
- changes to a few `.brand` (universal property) enum names (for compiler sanity)
- new setter in `historical` called `get_charging_sessions`
  - only "entry point" for requesting `charging_session` data
- removed `diagnostics.blind_spot_monitoring` in favour of `adas` properties

*Deprecated* properties:

- _ignition_
  - `accessories_status` in favour of `state`
  - `status` in favour of `state`
