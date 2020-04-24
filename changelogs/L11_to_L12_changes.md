# AutoAPI L12 Changelog
Level 12 contains a number of updates to the protocol, including new property components, changes to the spec and more.  

* [Spec Changes](#spec-changes)
  * [Renamed Fields](#renamed-fields)
  * [Misc Changes](#misc-changes)
* [Capabilities Changes](#capabilities-changes)
* [New Properties](#new-properties)
* [Deprecations](#deprecations)
* [Unit Component](#unit-component)
  * [Component](#component-unit)
  * [Spec Changes](#spec-changes)
* [Availability Component](#availability-component)
  * [Component](#component-availability)
  * [Availability Getters](#availability-getters)

## Spec Changes
### Renamed Fields

Some fields in the spec have been renamed for more consistency.

- changed `hex` to `data_component` in properties _examples_ (for consistency with new field names)
- changed `pretty_name` to `name_pretty` (for consistency with other `name_`-s)
- changed `unit` to `unit_sign` (to "free up" the _unit_ name for new purposes)
- changed `car_signature` to `vehicle_signature` (for semantic reasons)

### Misc Changes

There are a number of other miscellaneous changes:  

- added `internal_oem_error` to _failure reason_
  - in `failure_message` property `0x03`
  - in _failure component's_ `reason`
- moved files and definitions around for better organisation
  - all _capabilities_ definitions (files) are now in `capabilities/` folder
  - other spec files are moved to `misc/` folder
    - _property components_ are now defined in `property_components.yml`
    - _version_ is now defined in `version.yml` with a simpler structure (removed `identification`)
- changed references of _car_ to _vehicle_ to encompass a bigger range of machines

## Capabilities Changes

- **engine start stop** is removed
  - it's single property is moved to `engine` as a property named `start_stop_state`
- **vehicle status** is broken into two
  - new capability `vehicle_information` that contains the _static_ properties
  - old capability `vehicle_status` stays to output `states` properties

## New Properties

There are a number of new properties.  
A few are simply additive to the spec, some are from capabilities' changes and others are new because of the _unit component_ (see more [below](#unit-component)).

- **capabilities**
  - added `webhooks` - outputs _webhook_ information
- **charging**
  - added `battery_current` - outputs _electric current_ (i.e. `0.6A`)
  - added `charging_rate` - outputs _power_ (i.e. `150.31kW`)
  - added `charger_voltage` - outputs _voltage_ (i.e. `200V`)
  - added `current_type` - outputs _direct_ or _alternating current_ value
- **diagnostics**
  - added `engine_total_operating_time` - outputs _duration_ value (i.e. `8.1 weeks`)
  - added `odometer` - outputs _length_ value (i.e. `666.7km`)
- **engine**
  - added `start_stop_state` - outputs _active state_
- **home charger**
  - added `charging_power` - outputs _power_ value (i.e. `150.3kW`)
- **honk horn flash light**
  - added `honk_time` - outputs _duration_ value (i.e. `3.0s`)
- **maintenance**
  - added `distance_to_next_service` - outputs _length_ value (i.e. `332.2km`)
  - added `time_to_next_service` - outputs _duration_ value (i.e. `5.2 weeks`)
  - added `time_to_exhaust_inspection` - outputs _duration_ value (i.e. `345.6 days`)
- **usage**
  - added `odometer_after_last_trip` - outputs _length_ value (i.e. `15_678.9km`)
- **vehicle location**
  - added `precision` - outputs _length_ value (i.e. `100.0m`)
- **vehicle information**
  - added `power` - outputs _power_ value (i.e. `250.0kW`)
- **video handover**
  - added `starting_time` - outputs _duration_ value (i.e. `15.8s`)

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

## Unit Component
### Component<a name="component-unit"></a>

AutoAPI needs to dynamically output the _unit type_ of a property (or a custom type).  

For this reason, a new **optional** _property component_ called **unit component** is introduced to the protocol.    
It's ID is `0x04` and it follows the same header-payload structure as other components.  
Payload is 2 bytes referencing _measurement_ and _unit type_ from [unit_types.yml](https://github.com/highmobility/auto-api/blob/level12/misc/unit_types.yml).

Component structure:

```
[
 0x04,              - unit component ID
 0x00, 0x02,        - payload size
 measurement_type,  - measurement_type ID from unit_types.yml
 unit_type          - unit_type ID from the measurement_type sub-values
]
```

Example:

```
0x04        - ID for unit component
0x00, 0x02  - payload size is 2 bytes
0x12,       - measurement type is 'length'
0x0f        - unit type is 'scandinavian_miles'
```

### Spec Changes

The new unit component brings along some changes to _properties_ and _custom types_ spec.  

- added `unit_type` to express the type of _measurement_ the property outputs
- additions to `examples`
  - added `unit_component` to define the _hex_ value of the property
  - added `unit` to define the expected _unit type_ of the property
- changed properties with `unit_type`-field to be `type: double`
- deprecated properties with a specific unit in the name

## Availability Component
### Component<a name="component-availability"></a>

AutoAPI needs to support requesting and transmitting availability information for properties.  

To enable this, another _property component_ called **availability component** is introduced in L12.  
It's ID is `0x05` and payload is 10 bytes denoting the _update rate_ in relation to a trip, _rate limit_ and for what the rate limit applies to (i.e. `app` or `vehicle`).  

Component structure:  

```
[
 0x05,              - availability component ID
 0x00, 0x0a,        - payload size
 update_rate,       - update rate enum value
 rate_limit,        - rate limit frequency value
 applies_per        - rate limit applies per value
]
```

Example of _availability component_:

```
[
 0x05,                  - ID for availability component
 0x00, 0x0a,            - payload size is 10 bytes
 0x00,                  - update rate is 'trip_high' (data is updated with high frequency during a trip)
 0x4050000000000000,    - rate limit frequency is 64.0 (unit type comes from unit component)
 0x01                   - rate limit applies per 'vehicle'
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
