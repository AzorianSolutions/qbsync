# QBSync by [Azorian Solutions](https://azorian.solutions)

## How Does It Work?

The connectivity achieved with this link to Quickbooks Desktop is accomplished through the use of the
Quickbooks Web Connector (QBWC) software. Quickbooks Web Connector is a simple middleware that exposes the
Quickbooks Desktop local communication by calling a third-party SOAP API to check for instructions.

The QBSync application among other things, is that SOAP API that the Quickbooks Web Connector connects to. The QBWC
connects to the API and asks for any pending instructions. If there are any pending instructions, the QBWC sends them
to the Quickbooks Desktop software which then sends back a response to the QBWC when the request is done processing.

From there, the QBWC returns the response from Quickbooks Desktop to the QBSync SOAP API which signals QBSync to
process the result. For the last step, the QBSync application saves the received data from QBWC to the configured
target formats / locations.

## Getting started

The overall process to get this application deployed and working is fairly simple. Here are the high level steps with
supporting resources for additional information.

### Step 1. Quickbooks Web Connector Installation

Install the Quickbooks Web Connector to the computer running Quickbooks Desktop software. If you run multiple
workstations and use multi-user mode with some form of company file sharing, then install the Quickbooks Web Connector
on the primary desktop that acts as the host machine for Quickbooks Desktop.

Check out these additional resources for more information on installing the Quickbooks Web Connector or programming for
the qbXML SOAP API:

[Getting Started with QBWC](https://developer.intuit.com/app/developer/qbdesktop/docs/get-started/get-started-with-quickbooks-web-connector)

[QBWC Programm's Guide](https://static.developer.intuit.com/qbSDK-current/doc/pdf/QBWC_proguide.pdf)

### Step 2. QBSync Installation

Deploy the QBSync application to a Linux machine that the Quickbooks Web Connector has the ability to achieve
IPv4 communications with. Many Linux flavors come with Python already installed such as Ubuntu
[desktop](https://ubuntu.com/download/desktop) and [server](https://ubuntu.com/download/server)
environments. Assuming you have both Git and Python already installed, execute the following commands;

    git clone https://github.com/AzorianSolutions/as-apps-qbsync.git
    cd as-apps-qbsync
    pip install -r requirements.txt
    chmod +x admin.py run.py

### Step 3. Application Configuration

The default configuration is not ready to go out of the box. The default configuration is set to use "192.168.1.10" as
the hostname of the application. If this isn't updated before running the application, the resulting configuration
templates that generated will be wrong and cause the application to break. The port must also be configured to match
the configured port of the SOAP server. Unless you have a reverse proxy to funnel traffic through, the protocol
must remain as http as no SSL/TLS support is available in QBSync as this time.

Being that this application is designed for Linux environments but the Quickbooks Web Connector must run on Windows,
that means the QBSync app will need to be made available over a network.

How you go about this is your choice, but it is important to remember that this application was not designed with
public Internet communication in mind and thus doesn't boast the appropriate security to be available on the public
Internet. You can use IP restricted port forwarding or any number of tunneling options if the QBSync application must
be run on a remote network.

You also might have the ability to create an SSH port forwarding tunnel back to the QBSync Linux host from your Windows
machine running the Quickbooks Web Connector. Either way, the application must be bound to an interface accessible
outside the Linux host's loopback network.

You should also regenerate the password salt as is good security practice to not use a publicly disclosed salt.

For more information on configuring the application, read the [settings documentation](settings.md).

### Step 4. User Setup

To make user management a snap, I have provided an interactive CLI experience for managing application users. The
default configuration doesn't contain any users as this would require me to insecurely share the default passwords. You
should ideally create a new user for each unique machine that will run a copy of the Quickbooks Web Connector.

To create a new user, execute the following commands;

    cd {PROJECT_ROOT}
    ./admin.py -x add_user

For more information on using the admin CLI, read the [admin documentation](admin.md).

### Step 5. Starting the Application

    cd {PROJECT_ROOT}
    ./run.py

Now you should be able to access the HTTP interface of the application by navigating to http://localhost:8080.

By default, the QBWC SOAP API available at [http://localhost:8081/qbwc](http://localhost:8081/qbwc).

By default, you may also view the QBWC web service WSDL at
[http://localhost:8081/qbwc?wsdl](http://localhost:8081/qbwc?wsdl).
