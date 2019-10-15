# AutoAPI L11


The message types are now unified into 2 types.

* Get commands use `0x00`  
* Set commands use `0x01`  

Get commands allow a *state* to be queried (requested) from a connected device.  

Set commands allow *setting* of values, but also are used to transfer the *state* to the other device.  
It should be thought of as one device setting the data in the other one. What the receiving device then does with this data is up to the client / vehicle to decide.

The `.yml` spec files define the following *values* and *syntax* for each capability.  


## getters

If *not* defined in a capability – there are **no getters** for that capability.  
If defined, is a dictionary (hash) and requires 2 getters to be automatically synthesized following the pattern:

```
get_[cap.name]_state()                  --> [id.msb, id.lsb, 0x00]
get_[cap.name]_properties(property_IDs) --> [id.msb, id.lsb, 0x00] + property_IDs
```

The `_state` getter takes no input and requests **all** `state` properties in the capability.  
The `_properties` getter takes in *property IDs* as arguments and requests **only** those specified properties.  

There are additional *optional* keys available for getters:

* `name: string` used to override the *full name* of the getters (`_properties` still gets appended)  
* `skip_properties_getter: bool` used to skip the `_properties` getter generation  
    * If `false` (default), the `_properties` getter is **only** generated when there are **more than 1** property in the capability's `state`


Examples:

```yaml
getters: {}

getters:
    name: get_vehicle_location
    skip_properties_getter: true
    
getters:
    name: get_parking_ticket
```

Binary format:

```
> gets (requests) ALL the state-properties in a capability
[cap.msb, cap.lsb, 0x00]

> gets (requests) SPECIFIC state-properties in a capability
[cap.msb, cap.lsb, 0x00] + property_IDs

> examples
[0x00, 0x23, 0x00]                > get all Charging state-properties
[0x00, 0x23, 0x00] + [0x03, 0x0c] > get battery_level and charge_mode in Charging
```

## setters

If not defined in a capability – there are *no setters* for that capability.  
Otherwise, it's an array of dictionaries (hashes) as elements, with the dictionary having the following keys.  

The keys are divided into 2 categories: *required* and *optional* ones.  

Required keys:  

* `name: string` as the name of the setter

Optional keys (at least 1 has to be included; can be combined):  

* `mandatory: [property_IDs]` defines what properties are required as input (and what are actually sent in the setter)
* `optional: [property_IDs]` list of *optional* properties allowed as input. If only optional is defined (no *mandatory* or *constants*) - **at least 1** input is required
* `constants` is an array of constant values defined by the following keys:
    * `property_id: property_ID` defines the constant property
    * `value: [bytes]` lists the constant value of the property

Examples:

```yaml
setters:
  - name: start_stop_ionising
    mandatory: [0x08]
  - name: set_temperature_settings
    optional: [0x03, 0x04, 0x0c]
```  
```yaml
setters:
  - name: control_command
    optional: [0x02, 0x03]
  - name: start_control
    constants:
      - property_id: 0x01
        value: [0x02]
  - name: stop_control
    constants:
      - property_id: 0x01
        value: [0x05]
```

Binary format:

```
> set properties in a capability
[cap.msb, cap.lsb, 0x01] + properties_bytes

> examples
[0x00, 0x23, 0x01] + [0x0c, 0x00, 0x04, 0x01, 0x00, 0x01, 0x00] > set_charge_mode in Charging
```

## state

If not defined in a capability – there is **no state** for that capability.  
Defines what *properties* are exposed to the developer (client). This message is sent over the `set` message type.  

```
> receive properties (same binary as setters)
[id.msb, id.lsb, 0x01] + state_properties

> examples
[0x00, 0x23, 0x01] + [0x0c, 0x00, 0x04, 0x01, 0x00, 0x01, 0x00] > received charge_mode in Charging
```

Defines an array of *property IDs* (or keys).

* `all` noting that **all** properties in a state are exposed / included
* `[property_IDs]` defines what properties are exposed

Examples:  

```yaml
state: all
```
```yaml
state: [0x01, 0x02]
```


## properties

**Required** for every capability.  
Properties are used to transmit pieces of information.  

Each property can be either a **base** type or a **custom** type.  
*Base* types are defined in the *types section* below.  
*Custom* types are referenced from `custom_types.yml` in *capability* files with the syntax: `type: types.[name_of_custom_type]`  

Keys available for *all* properties:

* `id: integer` property identifier in hex
* `name: string` name of the property in *snake_case*
* `name_cased: string` name of the property in *camelCase*
* `type: string` type of the property

Other conditional keys:

* `size: integer` size of the property's *data component*
    * *only* present for *simple properties* (base-type) *and*
    * *only* present when the size is known in advance, i.e. *not* for a `string` or `bytes`
* `multiple: bool` if the property can occure multiple times in a command-state
    * defaults to `false`. If multiple is present, there is also the `name_singular` value that represents the name's 
    singular form
* `pretty_name: string` name of the property in a capitalised and whitespaced way, i.e. *Charging Power kW*
* `description: string` an explanation of the property (what it does, means or represents)
* `enum_values: []` a property can also be an `enum` – enums are explained in the *types section*

All single-`string` & `uinteger`-bytes properties derive their bytes count from the size of the property's *data component size*.

Examples:  

```yaml
properties:
  - id: 0x03
    name: model_name
    name_cased: modelName
    type: string
    description: The car model name bytes formatted in UTF-8
  - id: 0x07
    name: charger_voltage_dc
    name_cased: chargerVoltageDC
    pretty_name: Charger voltage (DC)
    type: float
    size: 4
    description: Charger voltage in 4-bytes per IEEE 754
  - id: 0x0b
    name: charge_port_state
    name_cased: chargePortState
    type: types.position
  - id: 0x11
    name: departure_times
    name_cased: departureTimes
    type: types.departure_time
    multiple: true
    name_singular: departure_time
```

Binary format:

```
> each property has 1-to-many property components
[prop.id, prop.size.msb, prop.size.lsb, 
  prop.component.id, prop.component.size.msb, prop.component.size.lsb, prop.component.value_bytes, 
  ...additional components]

> currently available PROPERTY COMPONENTS are
    0x01 - data component
    0x02 - timestamp component
    0x03 - failure component

> example
    0x0c        - property ID (Charging's charge_mode)
    0x00, 0x04  - property size
    0x01        - data component ID
    0x00, 0x01  - data component size
    0x00        - value (.immediate)
```

## types

Types follow the same pattern as *properties* - they all have the same *3 keys* as every property (except the `id`).  

**Base** types are simple types like `integer`, `uinteger`, `enum`, `float`, `double`, `string`, `bytes` and `timestamp`.

Types `string` and `bytes` can be considered *dynamic* by (usually) appearing without `size: x`.  
An example of the opposite would be *vehicleStatus.vin*

The `timestamp` type can be considered like an _alias_ to `uinteger` of
size 8.  
Its purpose is to allow developers to use the built-in
_DateTime_ data type where it exists.

Among these simple types, the `enum` is different to others.  
All enum types are actually a *1-byte size uinteger* values that **can** be used inside *single-type* properties too.  

Additional keys for `enum` types:  

* `enum_values: []` *every* enum type has an array of **cases** with the following keys:
    * `id: integer` case value in hex
    * `name: string` case name in *snake_case*
    * can additionally have the following keys:  
        * `pretty_name: string` case name capitalised and with whitespaces, i.e. *Plug-in Hybrid EV*
        * `verb: string` case name when used in an action (not that imporant), i.e. to *lock* a vehicle or *deactivate* smth
        * `disabled_in_setter: bool` defines what values are disallowed to use in a *setter* (the *lib* should check the input when combining the bytes for a command)

Examples:  

```yaml
  - name: active_state
    name_cased: activeState
    type: enum
    size: 1
    enum_values:
      - id: 0x00
        name: inactive
        verb: deactivate
      - id: 0x01
        name: active
        verb: activate

  - name: network_security
    name_cased: networkSecurity
    type: enum
    size: 1
    enum_values:
      - id: 0x00
        name: none
      - id: 0x01
        name: wep
        pretty_name: WEP
      - id: 0x02
        name: wpa
        pretty_name: WPA/WPA2 Personal
      - id: 0x03
        name: wpa2_personal
        pretty_name: WPA2 Personal
        
properties:
  - id: 0x17
    name: charging_state
    name_cased: chargingState
    type: enum
    size: 1
    enum_values:
      - id: 0x00
        name: not_charging
        verb: stop_charging
      - id: 0x01
        name: charging
        verb: start_charging
      - id: 0x02
        name: charging_complete
        disabled_in_setter: true
      - id: 0x03
        name: initialising
        disabled_in_setter: true
      - id: 0x04
        name: charging_paused
        disabled_in_setter: true
      - id: 0x05
        name: charging_error
        disabled_in_setter: true
```


**Custom** types are either commonly used types or ones with multiple pieces of information ordered in a specific byte sequence.  
Commonly used types are some `enum`-s and i.e. `timestamp`. Custom types are usually defined as `type: custom` and are *singular*.

Additional keys for `custom` types:  

* `items: []` *every* custom type has an ordered array of *items* that make up the type
    * consist of *base* or other *custom* types in byte order
    * `string` and `bytes` has an *implied* **2 byte size prefix** when inside a *custom* type

Examples:  

```yaml
  - name: action_item
    name_cased: actionItem
    type: custom
    items:
      - name: id
        name_cased: id
        pretty_name: ID
        type: uinteger
        size: 1
      - name: name
        name_cased: name
        type: string
        description: Name of the action
        
  - name: brake_torque_vectoring
    name_cased: brakeTorqueVectoring
    type: custom
    size: 2
    items:
      - name: axle
        name_cased: axle
        type: types.axle
      - name: state
        name_cased: state
        type: types.active_state
        
  - name: price_tariff
    name_cased: priceTariff
    type: custom
    items:
      - name: pricing_type
        name_cased: pricingType
        type: enum
        size: 1
        enum_values:
          - id: 0x00
            name: starting_fee
          - id: 0x01
            name: per_minute
          - id: 0x02
            name: per_kwh
            pretty_name: Per kWh
      - name: price
        name_cased: price
        type: float
        size: 4
        description: The price in 4-bytes per IEEE 754
      - name: currency
        name_cased: currency
        type: string
        description: The currency alphabetic code per ISO 4217 or crypto currency symbol
```

## examples

Every property has an array of examples (currently 1-2 for a given one).  
The examples are under the key `examples` and can also be used to generate *tests*.

Examples contain 3 parts:  

* `hex` has the hexadecimal value for the `data component` of the property
* `value(s)` contains the *parsed* value(s) of the hex
* `description` describes what the data represents (mostly used in doc-examples)

The *values* part has 2 mutually exclusive keys: `value` or `values`.  

`value` is used when the property has a "simple" type that only has a single value (i.e. an *integer*, *string*, *enum*).


```yaml
  - id: 0x01
    name: lock
    name_cased: lock
    type: types.lock_state
    examples:
      - hex: '00'
        value: 'unlocked'
        description: Trunk is unlocked

  - id: 0x07
    name: yaw_rate
    name_cased: yawRate
    type: float
    size: 4
    description: Yaw rate in degrees per second [°/s]
    examples:
      - hex: '40d51eb8'
        value: 6.66
        description: Yaw rate is 6.66 °/s
```

`values` is used for properties with *custom types* that contain more than 1 piece of distinct information (i.e. *time* with it's *hour* and *minute*).  
`values` contains a dictionary with keys as the names of the values in the *custom type*.

```yaml
  - id: 0x02
    name: persons_detected
    name_cased: personsDetected
    type: types.person_detected
    multiple: true
    name_singular: person_detected
    examples:
      - hex: '0001'
        values:
          location: 'front_left'
          detected: 'detected'
        description: Person detected on the front-left seat

  - id: 0x01
    name: accelerations
    name_cased: accelerations
    type: types.acceleration
    multiple: true
    name_singular: acceleration
    examples:
      - hex: '003f5d2f1b'
        values:
          direction: 'longitudinal'
          g_force: 0.864
        description: Longitudinal acceleration is 0.864 g
```


## miscellaneous

The *identifiers* and *API version* has been moved to new locations (structures).  
*Identifiers* are now defined like this:  

```yaml
identifier:
    msb: 0x00
    lsb: 0x35
```

And *API version* is defined so:  

```yaml
api:
    intro: 3
    update: 11
```

In addition, a new `disabled_in` structure for when a capability *isn't to be used* over some communication mediums:

```yaml
disabled_in: [ble, web]
```
