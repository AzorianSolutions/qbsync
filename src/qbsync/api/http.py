from loguru import logger


class HttpApi:

    @staticmethod
    def handle_requests():
        from src.qbsync.api.customers import CustomerApi
        from src.qbsync.api.invoices import InvoiceApi
        from src.qbsync.app import app

        logger.debug(f'Loading session queue from request queue.')

        handler_map = {
            'download_customers': CustomerApi.download,
            'download_invoices': InvoiceApi.download,
            'download_all': [CustomerApi.download, InvoiceApi.download]
        }

        # Check if any requests are in the request queue and load them into the session queue if so
        while not app.requests.empty():
            req = app.requests.get()
            req_type = req['job']

            # Validate the request type
            if req_type not in handler_map.keys():
                logger.warning(f'Unknown request type: {req_type}')
                continue

            logger.debug(f'Executing handler for {req_type} request type.')

            # Execute the request handler
            if hasattr(handler_map[req_type], '__call__'):
                handler_map[req_type]()
            elif isinstance(handler_map[req_type], list or tuple):
                for handler in handler_map[req_type]:
                    if hasattr(handler, '__call__'):
                        handler()
