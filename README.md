# nagios device check for nagios xi

Chef cookbook to install Nagios NRPE client (was previously part of the Nagios cookbook)

## Requirements

### NRPE

NRPE installed on windows machine

### Platform

- Windows 7/10

**Notes**: This script has been tested on the listed platforms. It may work on other platforms with or without modification.

## Service Configuration

### default

Installs the NRPE client via packages or source depending on platform and attributes set

### configure

Configures the NRPE client. 

## Attributes

### NRPE Configuration

- `NRPEClient++` - whether to install from package


### options for check

- `script ....` - options when installing nrpe via package manager. The default value for this attribute is nil.`

## Resources/Providers

#### Actions

#### Attribute Parameters

#### Examples

```python
# Use resource to define check_load

```

## License & Authors

- Author:: Meir Finkelstine [meirfi@outlook.com](mailto:meirfi@outlook.com)

```text
Copyright 2009-2017, My Compeny Software, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```