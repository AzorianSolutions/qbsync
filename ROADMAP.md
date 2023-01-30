# QBSync by [Azorian Solutions](https://azorian.solutions)

## Project Roadmap

### Releases

#### \> Ganymede 1.0.0 (current)

##### \+ Intuit Product Support
- Quickbooks Desktop

##### \+ Supported Data Entities
- Quickbooks Desktop
  - Customer
  - Invoice

##### \+ Supported Export Formats
- JSON
- YAML

##### \+ Supported Export Databases
- None

##### \+ New Features
- HTTP Interface
  - Ability to trigger entity download processes via HTTP interface
  - Ability to download QBWC QWC files for each QBSync user via HTTP interface
- SOAP Interface
  - Most of the current QBWC SOAP implementation is present in the current SOAP service.

#### \> Europa 1.1.0 (next)

##### \+ Intuit Product Support
- Quickbooks Desktop

##### \+ Supported Data Entities
- Quickbooks Desktop
  - Account
  - BarCode
  - Class
  - Company
  - Customer
  - Employee
  - DataExtDef
  - Invoice

##### \+ Supported Export Formats
- JSON
- YAML

##### \+ Supported Export Databases
- None

##### \+ New Features
- None

##### \+ Improvements
- Overhaul data entity translation system to be entirely schema definition based, requiring no code duplication
- Add the ability to override the data entity translation process with custom classes

#### \> Callisto 1.2.0 (future)

##### \+ Supported Data Entities
- Quickbooks Desktop
  - Account
  - BarCode
  - Class
  - Company
  - Customer
  - Employee
  - DataExtDef
  - Invoice

##### \+ Supported Export Databases
- MySQL
- PgSQL
- SQLite

##### \+ New Features
- Implement first pass of the data export to SQL databases feature.

##### \+ Improvements
Todo

#### \> Dia 1.3.0 (future)

##### \+ Supported Data Entities
- Quickbooks Desktop
  - All current entities supported.

##### \+ Supported Export Databases
- MySQL
- PgSQL
- SQLite
- MongoDB

##### \+ New Features
- Implement first pass of the data export to NoSQL databases feature.

##### \+ Improvements
Todo
