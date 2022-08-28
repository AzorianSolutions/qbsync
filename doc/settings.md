# QBSync by [Azorian Solutions](https://azorian.solutions)

## Application Settings

### - app

    id: UUID (V1 or V4)

The application's UUID which changes with every major release.

    name: String

The name of the application given in the QBWC configuration files generated for download.

    version: String (format: X.X.X)

The version of the current code base.

    protocol String (default: http, options: http, https)

The HTTP protocol that the QBWC application should use when connecting to the QBSync SOAP API.

    host String (default: 192.168.1.10, format: X.X.X.X or app.your.domain)

The host name that the QBWC application should use when connecting to the QBSync SOAP API.

    port Integer (default: 8081, minimum: 1, maximum: 63999)

The port number that the QBWC application should use when connecting to the QBSync SOAP API.

    support_url String (format: https://domain.name/request/uri)

The URL shown in the QBWC application for users to obtain additional support when using the QBSync application.

    run_interval Integer (default: 1, minimum: 1, maximum: 99999)

The number of seconds the QBWC application should wait between automatic requests to check with the QBSync application
for any new requests.

### - auth

    salt: String (minimum length: 0, maximum length: who knows)

The long and complicated string that should be used for salting user passwords before hashing.

    iterations: Integer (default: 10000, minimum: 1, maximum: what ever your machine can handle)

The number of hashing iterations to perform when hashing salted user passwords.

    users_path: String (default: users.yaml)

The absolute or relative (to the project root) path to the users YAML file.

### - servers

#### -- http

    host: String (default: 0.0.0.0, format: X.X.X.X)

The host IPv4 address to bind the HTTP server to. Set to 0.0.0.0 to bind to all available IPv4 addresses.

    port: Integer (default: 8080, minimum: 1, maximum: 63999)

The port number to bind the HTTP server to.

    debug: Boolean (default: false)

Whether to enable Flask debug mode when starting the HTTP server.

#### -- soap

    host: String (default: 0.0.0.0, format: X.X.X.X)

The host IPv4 address to bind the SOAP server to. Set to 0.0.0.0 to bind to all available IPv4 addresses.

    port: Integer (default: 8081, minimum: 1, maximum: 63999)

The port number to bind the SOAP server to.

### - api

#### -- customers

##### --- download

    page_size: Integer (default: 500, minimum: 1, maximum: test with caution)

The number of records to return in a single request batch when downloading all customer records.

#### -- invoices

##### --- download

    page_size: Integer (default: 500, minimum: 1, maximum: test with caution)

The number of records to return in a single request batch when downloading all invoice records.

### - export

    path: String

The absolute or relative (to the project root) directory path where file based data exports should be saved. 

#### -- types

##### --- customers

    - format: json
      name: customers.json

The data export configuration to save Quickbooks customer data in JSON format.

    - format: yaml
      name: customers.yaml

The data export configuration to save Quickbooks customer data in YAML format.

##### --- invoices

    - format: json
      name: invoices.json

The data export configuration to save Quickbooks invoice data in JSON format.

    - format: yaml
      name: invoices.yaml

The data export configuration to save Quickbooks invoice data in YAML format.

### - quickbooks

    company_file_path: String

The absolute path of the Quickbooks company file on the host system running Quickbooks Desktop software.

### - templates

    path: String (default: tpl)

The absolute or relative (to the project root) file system path to the template storage directory.

    error: String (default: error.html)

The relative (to the template storage directory) file system path to the error HTML template.

    qbwc: String (default: qbsync.qwc)

The relative (to the template storage directory) file system path to the QBWC configuration template.
