from loguru import logger
from spyne import Array, Integer, Unicode, ServiceBase
from spyne.protocol.soap import Soap11
from flask import Flask
from flask_spyne.flask_spyne import Spyne
import time

app = Flask(__name__)
spyne = Spyne(app)


class QuickbooksService(ServiceBase):
    __target_namespace__ = 'http://developer.intuit.com/'
    __service_url_path__ = '/qbwc'
    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = Soap11()

    @spyne.srpc(Unicode, Unicode, _returns=Array(Unicode))
    def authenticate(strUserName, strPassword):
        import hashlib
        from src.qbsync.api.http import HttpApi
        from src.qbsync.app import app
        from src.qbsync.request_manager import manager as session_manager
        """Authenticate the Quickbooks Web Connector to this web service.
        @param strUserName username to use for authentication
        @param strPassword password to use for authentication
        @return the response array
        """

        # Trigger the HTTP API to execute any pending request handlers that typically register QBWC requests
        HttpApi.handle_requests()

        conf = app.config['defaults']['quickbooks']
        response = []
        authenticated: bool = False
        queue_item = session_manager.get_next_request()

        # Salt / hash the provided password for comparison
        salt = app.config['defaults']['auth']['salt']
        iterations = app.config['defaults']['auth']['iterations']
        digest = hashlib.pbkdf2_hmac('sha256', strPassword.encode(), str(salt).encode(), iterations)

        # QBWC username not found
        if strUserName not in app.users:
            logger.warning(f'Quickbooks Web Connector authentication denied for invalid username of {strUserName}.')
            response.append('NVU')
            response.append('')
            response.append(1)

        # QBWC password mismatch
        elif digest.hex() != app.users[strUserName]:
            logger.warning(f'Quickbooks Web Connector authentication denied for invalid password for username of'
                           + f' {strUserName}.')
            response.append('NVU')
            response.append('')
            response.append(1)

        # QBWC successfully authenticated
        else:
            authenticated = True
            logger.info(f'Quickbooks Web Connector request authenticated at {time.ctime()}')

        # No requests in the queue
        if authenticated and not isinstance(queue_item, dict):
            response.append("NONE")
            response.append("NONE")

        # Requests in the queue
        elif authenticated:
            response.append(queue_item['request_id'] if queue_item['request_id'] is not None else '')
            response.append(conf['company_file_path'])
            response.append(str(queue_item['update_pause']))
            response.append(str(queue_item['minimum_update']))
            response.append(str(queue_item['minimum_run_interval']))

        return response

    @spyne.srpc(Unicode, _returns=Unicode)
    def clientVersion(strVersion):
        """ sends Web connector version to this service
        @param strVersion version of GB web connector
        @return empty string
        """
        logger.debug(f'QBWC reported software version {strVersion}.')
        return ""

    @spyne.srpc(Unicode, _returns=Unicode)
    def getServerVersion(ticket):
        from src.qbsync.app import app
        """ sends application version of this server
        @return the current version of this application
        """
        logger.debug(f'QBWC requested server version.')
        return str(app.config['defaults']['app']['version'])

    @spyne.srpc(Unicode, _returns=Unicode)
    def closeConnection(ticket):
        """ used by web connector to indicate it is finished with update session
        @param ticket session token sent from this service to web connector
        @return string displayed to user indicating status of web service
        """
        logger.debug(f'QBWC closed connection for request {ticket}.')
        return "OK"

    @spyne.srpc(Unicode, Unicode, Unicode, _returns=Unicode)
    def connectionError(ticket, hresult, message):
        """ used by web connector to report errors connecting to Quickbooks
        @param ticket session token sent from this service to web connector
        @param hresult The HRESULT (in HEX) from the exception
        @param message error message
        @return string done indicating web service is finished.
        """
        logger.error(f'QBWC encountered an error with Quickbooks for request {ticket} ({hresult}): {message}')
        return "done"

    @spyne.srpc(Unicode, _returns=Unicode)
    def getLastError(ticket):
        """ Used by QBWC to retrieve the last error that occurred following an operation.
        @param ticket session token sent from this service to web connector
        @return string displayed to user indicating status of web service
        """
        logger.debug(f'QBWC requested last operational error for request {ticket}.')
        return ""
        # return "NoOp"

    @spyne.srpc(Unicode, Unicode, Unicode, Unicode, Integer, Integer, _returns=Unicode)
    def sendRequestXML(ticket, strHCPResponse, strCompanyFileName, qbXMLCountry, qbXMLMajorVers, qbXMLMinorVers):
        from src.qbsync.request_manager import manager as session_manager
        """ send request via web connector to Quickbooks
        @param ticket session token sent from this service to web connector
        @param strHCPResponse qbXML response from QuickBooks
        @param strCompanyFileName The Quickbooks file to get the data from
        @param qbXMLCountry the country version of QuickBooks
        @param qbXMLMajorVers Major version number of the request processor qbXML
        @param qbXMLMinorVers Minor version number of the request processor qbXML
        @return string containing the request if there is one or a NoOp
        """
        logger.debug(f'QBWC requested next queue item for request {ticket}.')
        request = session_manager.get_current_request(ticket)

        return request if isinstance(request, bytes) else ''

    @spyne.srpc(Unicode, Unicode, Unicode, Unicode, _returns=Integer)
    def receiveResponseXML(ticket, response: str or None, hresult, message):
        from src.qbsync.request_manager import manager
        """ Returns the data request response from QuickBooks or QuickBooks POS.
        @param ticket The ticket from the web connector. 
        @param response Contains the qbXML response from QuickBooks or qbposXML response from QuickBooks POS.
        @param hresult A hex value indicating an error code for the current request.
        @param message A string containing an error message for the current request.
        @return integer A positive integer less than 100 represents the percentage of work completed.
        """
        logger.debug(f'QBWC sent response for queue item with request {ticket} ({hresult}): {message}.')

        if isinstance(response, str) and len(response.strip()):
            manager.handle_response(ticket, response)

            # Return a value between 1 and 100 indicating the percent complete that the current request cycle is
            return 10
        else:
            return 0
