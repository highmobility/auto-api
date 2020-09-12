# AutoAPI L12 Changelog

Level 12 contains a number of updates to the protocol.  

**These include**:  
- new capability for static vehicle information (properties split from `vehicle_status`)  
- new type of value to dynamically transfer values in different units  
- new property component to output availability information for a given datapoint  
- new properties to go along with the _unit type_  
- new deprecation structure to ease the pain of future API changes  
- changes to fields in spec to foster consistency  
- other minor changes  

Changes from L11 are divided into these sub-sections:
* [Spec Changes](#spec-changes)
  * [Renamed Fields](#renamed-fields)
  * [Misc Changes](#misc-changes)
* [Capabilities Changes](#capabilities-changes)
* [New](#new)
  * [Properties](#properties)
  * [Custom Types](#custom-types)
  * [Universal Properties](#universal-properties)
* [Deprecations](#deprecations)
* [Updated Properties](#updated-properties)
* [Unit Type](#unit-type)
  * [Type](#component-type)
  * [Spec Changes](#unit-type-spec-changes)
* [Availability Component](#availability-component)
  * [Component](#component-availability)
  * [Availability Getters](#availability-getters)

## Spec Changes
### Renamed Fields

Some fields in the spec have been renamed for more consistency.

- changed `hex` to `data_component` in properties _examples_ (for consistency with new field names)
- changed `pretty_name` to `name_pretty` (for consistency with other `name_`-s)
- changed `car_signature` to `vehicle_signature` (for semantic reasons)

### Misc Changes

There are a number of other miscellaneous changes:  

- added `internal_oem_error` to _failure reason_
  - in `failure_message` property `0x03`
  - in _failure component's_ `reason`
- moved files and definitions around for better organisation
  - all _capabilities_ definitions (files) are now in [`capabilities/`](https://github.com/highmobility/auto-api/tree/level12/capabilities) folder
  - other spec files are moved to [`misc/`](https://github.com/highmobility/auto-api/tree/level12/misc) folder
    - _property components_ are now defined in [`property_components.yml`](https://github.com/highmobility/auto-api/blob/level12/misc/property_components.yml)
    - _version_ is now defined in [`version.yml`](https://github.com/highmobility/auto-api/blob/level12/misc/version.yml) with a simpler structure (removed `identification: version`)
- changed references of _car_ to _vehicle_ to encompass a bigger range of machines
- _brand_ and _vin_ moved to _universal properties_

> :warning: **Dynamic property subtypes**
>
> When a property contains a subtype that is dynamic (i.e. `key_value`), then the _subtype_ is **prefixed** with _2 bytes_ denoting it's size. 

Example:

```
0x24,                   - diagnostics 'oem_trouble_code_values' property ID
0x00, 0x24,             - property size is 36 bytes

0x01,                   - data component ID
0x00, 0x21,             - data component size is 33 bytes

0x00, 0x05,             - 'id' item string-size prefix is 5 bytes
0x3132334944,           - 'id' string value is '123ID'

0x00, 0x18,             - 'key_value' item-size prefix (because it's dynamic) is 24 bytes

0x00, 0x0a,             - 'key' item (in 'key_value' type) string-size prefix is 10 bytes
0x736f6d655f6572726f72, - 'key' string value is 'some_error'

0x00, 0x0a,             - 'value' item (in 'key_value' type) string-size prefix is 10 bytes
0x736f6d655f76616c7565  - 'value' string value is 'some_value'
```

## Capabilities Changes

- **engine start stop** is removed
  - it's single property is moved to `engine` as a property named `start_stop_state`
- **vehicle status** is broken into two
  - new capability `vehicle_information` that contains the _static_ properties
  - old capability `vehicle_status` stays to output `states` properties

## New
### Properties

There are a number of new properties.  
A few are simply additive to the spec, some are from capabilities' changes and others are new because of the _unit type_ (see more [below](#unit-type)).

- **capabilities**
  - added `webhooks` - outputs _webhook_ information
- **charging**
  - added `battery_current` - outputs _electric current_ (i.e. `0.6A`)
  - added `charging_rate` - outputs _power_ (i.e. `150.31kW`)
  - added `charger_voltage` - outputs _voltage_ (i.e. `200V`)
  - added `current_type` - outputs _direct_ or _alternating current_ value
  - added `max_range` - outputs maximum electric range
  - added `starter_battery_state` - outputs state of the starter battery
  - added `smart_charging_status` - outputs status of optimized/intelligent charging
  - added `battery_level_at_departure` - outputs battery charge level expected at time of departure
  - added `preconditioning_departure_status` - outputs status of preconditioning at departure time
  - added `preconditioning_immediate_status` - outputs status of immediate preconditioning
  - added `preconditioning_departure_enabled` - outputs preconditioning activation status at departure
  - added `preconditioning_error` - outputs preconditioning error if one is encountered
- **diagnostics**
  - added `engine_total_operating_time` - outputs _duration_ value (i.e. `8.1 weeks`)
  - added `odometer` - outputs _length_ value (i.e. `666.7km`)
  - added `tire_pressure_statuses` - outputs tire pressures status'
  - added `brake_lining_wear_pre_warning` - outputs status of brake lining wear pre-warning
  - added `engine_oil_life_remaining` - outputs remaining life of engine oil which decreases over time
  - added `oem_trouble_code_values` - outputs additional OEM trouble codes
  - added `diesel_exhaust_fluid_range` - outputs distance remaining until diesel exhaust fluid is empty
  - added `diesel_particulate_filter_soot_level` - outputs level of soot in diesel exhaust particulate filter
- **engine**
  - added `start_stop_state` - outputs _active state_
- **home charger**
  - added `charging_power` - outputs _power_ value (i.e. `150.3kW`)
- **honk horn flash light**
  - added `honk_time` - outputs _duration_ value (i.e. `3.0s`)
- **ignition**
  - added `state` - outputs the ignition state
- **lights**
  - added `switch_position` - outputs position of the rotary light switch
- **maintenance**
  - added `distance_to_next_service` - outputs _length_ value (i.e. `332.2km`)
  - added `time_to_next_service` - outputs _duration_ value (i.e. `5.2 weeks`)
  - added `time_to_exhaust_inspection` - outputs _duration_ value (i.e. `345.6 days`)
  - added `last_ecall` - outputs date-time of the last eCall
- **rooftop control**
  - added `sunroof_rain_event` - outputs sunroof event happened in case of rain
- **theft alarm**
  - added `interior_protection_status` - outputs interior protection sensor status
  - added `tow_protection_status` - outputs tow protection sensor status
  - added `last_warning_reason` - outputs last warning reason
  - added `last_event` - outputs last event happening date
  - added `last_event_level` - outputs level of impact for the last event
  - added `event_type` - outputs position of the last even relative to the vehicle
- **trips (new capa)**
  - added `type` - outputs type of the trip
  - added `driver_name` - outputs driver name
  - added `description` - outputs description of the trip
  - added `start_time` - outputs start time of the trip
  - added `end_time` - outputs end time of the trip
  - added `start_address` - outputs start address of the trip
  - added `end_address` - outputs end address of the trip
  - added `start_coordinates` - outputs start coordinates of the trip
  - added `end_coordinates` - outputs end coordinates of the trip
  - added `start_odometer` - outputs odometer reading at the start of the trip
  - added `end_odometer` - outputs odometer reading at the end of the trip
  - added `average_fuel_consumption` - outputs average fuel consumption during the trip
  - added `distance` - outputs distance of the trip
  - added `start_address_components` - outputs start address components
  - added `end_address_components` - outputs end address components
- **usage**
  - added `odometer_after_last_trip` - outputs _length_ value (i.e. `15_678.9km`)
  - added `safety_driving_score` - outputs safety driving score as percentage
  - added `rapid_acceleration_grade` - outputs grade given for rapid acceleration over time
  - added `rapid_deceleration_grade` - outputs grade given for rapid deceleration over time
  - added `late_night_grade` - outputs grade given for late night driving over time
  - added `distance_over_time` - outputs distance driven over a given time period
  - added `electric_consumption_rate_since_start` - outputs electric energy consumption rate since the start of a trip
  - added `electric_consumption_rate_since_reset` - outputs electric energy consumption rate since a reset
  - added `electric_distance_last_trip` - outputs distance travelled with electricity in last trip
  - added `electric_distance_since_reset` - outputs distance travelled with electricity since reset
  - added `electric_duration_last_trip` - outputs duration of travelling using electricity during last trip
  - added `electric_duration_since_reset` - outputs duration of travelling using electricity since reset
  - added `fuel_consumption_rate_last_trip` - outputs liquid fuel consumption rate during last trip
  - added `fuel_consumption_rate_since_reset` - outputs liquid fuel consumption rate since reset
  - added `average_speed_last_trip` - outputs average speed during last trip
  - added `average_speed_since_reset` - outputs average speed since reset
  - added `fuel_distance_last_trip` - outputs distance travelled with (liquid) fuel during last trip
  - added `fuel_distance_since_reset` - outputs distance travelled with (liquid) fuel since reset
  - added `driving_duration_last_trip` - outputs duration of last trip
  - added `driving_duration_since_reset` - outputs duration of travelling since reset
  - added `eco_score_total` - outputs overall eco-score rating
  - added `eco_score_free_wheel` - outputs eco-score rating for free-wheeling
  - added `eco_score_constant` - outputs eco-score constant
  - added `eco_score_bonus_range` - outputs eco-score bonus range
- **vehicle information (new capa)**
  - added `power` - outputs _power_ value (i.e. `250.0kW`)
  - added `language` - outputs the language on headunit
  - added `timeformat` - outputs the timeformat on headunit
- **vehicle location**
  - added `precision` - outputs _length_ value (i.e. `100.0m`)
- **video handover**
  - added `starting_time` - outputs _duration_ value (i.e. `15.8s`)
  
### Custom Types

- added `active_selected_state`
- added `grade`
- added `key_value`
- added `location_wheel`
- added `weekday`
- added `address_component`
- added `availability`
- added `distance_over_time`
- added `failure`
- added `oem_trouble_code_value`
- added `tire_pressure_status`
- added `webhook`

Also, L12 updated some values (i.e. enum added new enum values).

- updated `dashboard_lights`
- updated `trouble_code`

### Universal Properties

Two properties from _vehicle status_ are moved to _universal properties_ (meaning they can be transmitted with every property).  

- added `vin` - outputs the VIN of the unique Vehicle Identification Number
- added `brand` - outputs the vehicle brand

## Deprecations

New fields for properties to enable easier modifications to the spec (interface) while live systems migrate to new versions.  
_Deprecated properties could be removed with next versions of AutoAPI without additional warnings._

Fields added to _deprecated_ properties:

```
deprecated:
  new_name: name of the new property that this is deprecated in favour of
  reason: reason for the deprecation
```

Currently deprecated properties are (mainly) those that contained a _unit_ in the name.  
List of deprecated properties:

- **charging**
  - deprecated `battery_current_ac` in favour of `battery_current` and `current_type`
  - deprecated `battery_current_dc` in favour of `battery_current` and `current_type`
  - deprecated `charger_voltage_ac` in favour of `charger_voltage ` and `current_type`
  - deprecated `charger_voltage_dc` in favour of `charger_voltage ` and `current_type`
  - deprecated `charging_rate_kw` in favour of `charging_rate`
- **diagnostics**
  - deprecated `engine_total_operating_hours` in favour of `engine_total_operating_time`
  - deprecated `mileage` in favour of `odometer`
  - deprecated `mileage_meters` in favour of `odometer`
- **home charger**
  - deprecated `charging_power_kw` in favour of `charging_power`
- **honk horn flash lights**
  - deprecated `honk_seconds` in favour of `honk_time`
- **maintenance**
  - deprecated `days_to_next_service` in favour of `time_to_next_service`
  - deprecated `kilometers_to_next_service` in favour to `distance_to_next_service`
  - deprecated `months_to_exhaust_inspection` in favour of `time_to_exhaust_inspection`
- **usage**
  - deprecated `mileage_after_last_trip` in favour of `odometer_after_last_trip`
- **vehicle information**
  - deprecated `power_in_kw` in favour of `power`
- **video handover**
  - deprecated `starting_second` in favour of `starting_time`
  
## Updated Properties

Some properties have updated values (i.e. new enum values added).  

- **charging**
  - updated `status` - added new enum values

## Unit Type
### Type<a name="component-type"></a>

AutoAPI needs to dynamically output the _unit type_ of a value.  

For this reason, a new sort of `type` is added to the protocol.  
When a value expresses a _unit_, it's type will be defined as `type: unit.xxx`, where the _xxx_ is a reference to a _measurement type_.

Value of _unit_ type will be **10 bytes** long.  
First **2 bytes** denoting the _measurement type_ and _unit type_ referenced from [unit_types.yml](https://github.com/highmobility/auto-api/blob/level12/misc/unit_types.yml).  
The remaining **8 bytes** will form a _double_ value.

Value's bytes structure:

```
[
 measurement_type,  - measurement_type ID from unit_types.yml
 unit_type          - unit_type ID from the measurement_type sub-values
 ...                - remaining 8 bytes for a DOUBLE
]
```

Bytes example:

```
0x12,               - measurement type is 'length'
0x07                - unit type is 'millimeters'
0x4039666666666666  - 25.4
```

Spec example:

```
id: 0x08
name: current_chassis_position
...
type: unit.length
size: 10
...
```

### Spec Changes<a name="unit-type-spec-changes"></a>

The new unit type brings along some changes to _properties_ and _custom types_ spec.  

- added new `type: unit.xxx` to express the type of _measurement_ the property outputs
- additions to `examples`
  - values with a _unit_ are now expressed as `value: millimeters: 25.4`
- deprecated properties with a specific unit in the name

## Availability Component
### Component<a name="component-availability"></a>

AutoAPI needs to support requesting and transmitting availability information for properties.  

To enable this, another _property component_ called **availability component** is introduced in L12.  
It's ID is `0x05` and payload is 12 bytes denoting the _update rate_ in relation to a trip, _rate limit_ and for what the rate limit applies to (i.e. `app` or `vehicle`).  

Component structure:  

```
[
 0x05,              - availability component ID
 0x00, 0x0c,        - payload size
 update_rate,       - update rate enum value
 rate_limit,        - rate limit frequency value
 applies_per        - rate limit applies per value
]
```

Example of _availability component_:

```
[
 0x05,                      - ID for availability component
 0x00, 0x0c,                - payload size is 12 bytes
 0x00,                      - update rate is 'trip_high' (data is updated with high frequency during a trip)
 0x0e044050000000000000,    - rate limit frequency is 64.0Hz
 0x01                       - rate limit applies per 'vehicle'
]
```

### Availability Getters
Furthermore, to request _availability_ information for a given property, a new _message type_ `0x02` is added.  

This behaves the same way as _getters_ using `0x00`, but instead of requesting the _data component_, it requests the **availability component**.  
The _"availability getters"_ should be generated by the same rules as _"normal getters"_.  

Examples:

```
[0x00, 0x23, 0x02]              - request all properties in 'charging'  
[0x00, 0x23, 0x02, 0x03, 0x04]  - request specific properties in 'charging'
```
