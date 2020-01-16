# AutoAPI

The Auto API is a list of predefined APIs for cars which follow a coherent structure.

The `.yml` spec files define each capability (API).  

Table of contents
=================
<!--ts-->
   * [Overview](#overview)
      * [Capabilities](#capabilities)
      * [Properties](#properties)
   * [Features](#features)
   * [Getting Started](#getting-started)
      * [Documentation](#documentation)
   * [Contributing](#contributing)
   * [Licence](#licence)
<!--te-->


## Overview

#### Capabilities

The API is divided into `capabilities` that group together APIs with similar semantics.  

A capability could have:  

- *state* - transmitted from the vehicle to a connected device
- *getters* - requesting information from the vehicle
- *setters* - sending commands to the vehicle

Every capability defines a set of `properties` that are grouped together to create the API components (commands) above.

#### Properties

`Properties` are used as the basic building blocks to transmit data and can additionally consist of *failure* and/or *timestamp* components.  

Each property defines itself with:  

- *identifier* - property ID that's unique in a capability (also used to request specific data from the vehicle)
- *size* - size of the components
- *components...* - like *data* and *timestamp*


Please find more info about the properties in the [spec](https://github.com/highmobility/auto-api/tree/master/SPEC.md#properties).



## Features

**Generatable**: From version L11, the spec is written to encourage automatic generation of platform native libs (by creating a parser for that).

**Dynamic**: The definitions can be easily updated and dependent libs regenerated. When only adding capabilities and properties - older libs-parsers work as before.

**Modular**: The data flow is designed to be modular, while still trying to keep the package size small for the benefit of low-bandwith connections.


## Getting started

Get started by reading the [AutoAPI guide](https://high-mobility.com/learn/tutorials/getting-started/auto-api-guide/) in high-mobility.com.  

Check out the [spec](https://github.com/highmobility/auto-api/tree/master/SPEC.md) for more details on the structure and logic, or some libs generatated on this spec: [iOS](https://github.com/highmobility/auto-api-swift), [Android](https://github.com/highmobility/hm-java-auto-api), [Elixir](https://github.com/highmobility/hm-auto-api-elixir).  


### Documentation

Documentation at [high-mobility.com](https://high-mobility.com/learn/) is also generated based on this spec and combines all the information into a more readable form.  
When not implementing this spec directly, the site above is *recommended* as the main reference point to the API.

Some capabilities to check out from there: [Charging](https://high-mobility.com/learn/documentation/auto-api/chassis/charging/), [Doors](https://high-mobility.com/learn/documentation/auto-api/digital-key/doors/), [Vehicle Location](https://high-mobility.com/learn/documentation/auto-api/points-of-interest/vehicle-location/) and [Vehicle Status](https://high-mobility.com/learn/documentation/auto-api/api-structure/vehicle-status/).


## Contributing

We would love to accept your patches and contributions to this project. Before getting to work, please first discuss the changes that you wish to make with us via [GitHub Issues](https://github.com/highmobility/auto-api/issues), [Spectrum](https://spectrum.chat/high-mobility/) or [Slack](https://slack.high-mobility.com/).

See more in [CONTRIBUTING.md](https://github.com/highmobility/auto-api/tree/master/CONTRIBUTING.md)


## Licence

This repository is using MIT licence. See more in [LICENCE](https://github.com/highmobility/auto-api/tree/master/LICENCE)
