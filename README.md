# AutoAPI L11


The message types are now unified into 2 types.

* Get commands use `0x00`  
* Set commands use `0x01`  

Get commands allow a *state* to be queried (requested) from a connected device.  

Set commands allow *setting* of values, but also are used to transfer the *state* to the other device.  
It should be thought of as one device setting the data in the other one. What the receiving device then does with this data is up to the client / vehicle to decide.

The `.yml` spec files define the following *values* and *syntax* for each capability.  


## getters

If not defined in a capability – there are *no getters* for that capability.  
Otherwise, it's a dictionary (hash) with 2 possible keys.

* `default` marks the capability having *default getters*
* `static` defines a getter that requests *specific properties*

### default

Requires 2 getters to be automatically synthesised.

```
get_[name]_state()                  --> [id.msb, id.lsb, 0x00]
get_[name]_properties(property_IDs) --> [id.msb, id.lsb, 0x00] + property_IDs
```

The `_state` getter takes no input and requests **all** properties in the capability.  
The `_properties` getter takes in *property IDs* as arguments and requests **only** the specific properties.  

There are additional customisation options available for getters:

* `name_override: string` used to override the `[name]` in the getters generation
* `omit_state_text: bool` used to remove the `_state` text from the *state-getter*
* `skip_properties_getter: bool` used to skip the `_properties` getter generation
	* If `false` (default), the `_properties` getter is **only** generated when there are **more than 1** property in the capability

Examples:

```yaml
getters:
    default
```  
```yaml
getters:
    default:
        name_override: vehicle_location
        omit_state_text: true
```  
```yaml
getters:
    default:
        omit_state_text: true
        skip_properties_getter: true
```

### static

Defines *static* getters, that always request *specific properties*, to be automatically synthesised.  

```
get_[name]()    --> [id.msb, id.lsb, 0x00] + property_IDs
```

Contains an array of *static* getters that have the following keys-values:

* `name: string` as the name of the getter
* `properties: [property_IDs]` defines what properties the getter requests

Examples:  

```yaml
getters:
    static:
      - name: get_control_mode
        properties: [0x01]
      - name: some_other_getter
        properties: [0x02, 0x03]
```


## commands

If not defined in a capability – there are *no commands* for that capability.  
Otherwise, it's an array of dictionaries (hashes) as elements, with the dictionary having the following keys.  

The keys are divided into 2 categories: *required* and *optional* ones.  

Required keys:  

* `name: string` as the name of the setter

Optional keys (at least 1 has to be included; can be combined):  

* `mandatory: [property_IDs]` defines what properties are required as input (and what are actually sent in the command)
* `optional: [property_IDs]` list of *optional* properties allowed as input, if only this is defined (no *mandatory* or *constants*) - **at least 1** input is required
* `constants` is an array of constant values defined by the following keys:
    * `property_id: property_ID` defines the constant property
    * `value: [bytes]` lists the constant value of the property

Examples:

```yaml
commands:
  - name: start_stop_ionising
    mandatory: [0x08]
  - name: set_temperature_settings
    optional: [0x03, 0x04, 0x0c]
```  
```yaml
commands:
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


## state

If not defined in a capability – there are *no states* for that capability.  
Defines what *properties* are exposed to the developer (client). This message is sent over the `set` message type.  

```
[id.msb, id.lsb, 0x01] + state_properties
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
Follows the same syntax as before, with some additional options for *enums*.  

* `id: integer` identifier, required (if a *property* or an *enum value*)
* `name: string` name of the property / type, required
* `type: string` type of the property / item, required
* `size: integer` size of the item, required (if the type isn't *string* or it doesn't have *dynamic* values)
* `[flags]` define additional options for the property (i.e. `multiple: true`), optional
* `[texts]` means other *text* related things (i.e. `pretty_name: string`, `description: string`), optional
* `values/items` array of values / items that define the data structure in the property (same as previous versions), required

*New* keys for `enum` types.  

* `disabled_in_command: bool` defines what values are disallowed to use in a *command* (that uses that property)
* `verb: string` used to express an action in a *command* or used as another name (i.e. *active - activate*, *triggered - trigger* )
* `verb_pretty_name: string` defines the "pretty" name of the *verb*

Examples:  

```yaml
properties:
  - id: 0x02
    name: action_items
    type: custom
    multiple: true
    items:
      - name: identifier
        type: integer
        size: 1
      - name: name
        type: string
        description: Name of the action, bytes in UTF8.
  - id: 0x03
    name: convertible_roof_state
    type: enum
    size: 1
    values:
      - id: 0x00
        name: closed
        verb: close
      - id: 0x01
        name: open
      - id: 0x02
        name: emergency_locked
        disabled_in_command: true
      - id: 0x03
        name: closed_secured
        disabled_in_command: true
  - id: 0x1c
    name: wheel_rpms
    type: custom
    size: 3
    multiple: true
    pretty_name: Wheel RPMs
    items:
      - name: location
        type: enum
        size: 1
        values:
          - id: 0x00
            name: front_left
          - id: 0x01
            name: front_right
          - id: 0x02
            name: rear_right
          - id: 0x03
            name: rear_left
      - name: rpm
        type: integer
        size: 2
        pretty_name: RPM
        description: The RPM measured at this wheel
```


## miscellaneous

New *types* for properties.  

* `timestamp` is used in all our *timestamp* / *date* related properties / types (used to be `integer: 8`)
* `signal` used to convey a single action that doesn't have any value (empty *property data component*; i.e. *wake_up*, *clear_notification*)
* `custom` used when the property contains `items` (meaning it's a custom structure defined by us)
* `capability_state` represents a state of a capability (i.e. *states* in *vehicle status*)

In addition, the *identifiers* and *API version* has been moved to new locations (structures).  
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
