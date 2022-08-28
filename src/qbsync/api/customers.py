from loguru import logger
from src.qbsync.api.base import BaseApi


class CustomerApi(BaseApi):
    DATA_TYPE = 'customers'

    @staticmethod
    def download():
        logger.debug(f'Downloading Quickbooks customer data.')

        # Clear any lingering records from the download queue
        CustomerApi.empty_queue()

        # Set up first download request
        request = CustomerApi.build_list_request()

        # Queue the download request
        CustomerApi.queue_request(request=request, callback=CustomerApi.receive_download)

    @staticmethod
    def receive_download(request_id: str or None, response: str or None):
        from lxml import etree

        if not isinstance(response, str) or not len(response.strip()):
            return

        # Queue the response for processing after downloading is complete
        CustomerApi.queue_response(response)

        # Extract the total remaining records for the iterator from the response
        root = etree.fromstring(response)
        remaining_search = root.xpath('//CustomerQueryRs/@iteratorRemainingCount')
        total_remaining: int = 0
        if isinstance(remaining_search, list) and len(remaining_search):
            total_remaining = int(remaining_search[0])

        logger.debug(f'Total Downloads Remaining: {total_remaining}')

        # Setup additional download request when the iterator has additional records
        if total_remaining:
            req_id = int(root.xpath('//CustomerQueryRs/@requestID')[0]) + 1
            iterator_id = root.xpath('//CustomerQueryRs/@iteratorID')[0]

            # Set up the download request
            request = CustomerApi.build_list_request(request_id=req_id, iterator_id=iterator_id)

            # Queue the download request
            CustomerApi.queue_request(request=request, callback=CustomerApi.receive_download, request_id=request_id)

        # Process response data now that there are no remaining records to be downloaded
        else:
            CustomerApi.save_queue(CustomerApi.DATA_TYPE)

    @staticmethod
    def build_list() -> list:
        import xmltodict
        from src.qbsync.mutables.customer import CustomerMutable
        from src.qbsync.mutables.customer_address import CustomerAddressMutable
        from src.qbsync.mutables.customer_shipping_address import CustomerShippingAddressMutable

        data: list = []

        # Process queued download responses sequentially
        for response in CustomerApi.get_queue():
            doc = xmltodict.parse(response)

            if 'CustomerRet' not in doc["QBXML"]["QBXMLMsgsRs"]["CustomerQueryRs"]:
                continue

            records = doc["QBXML"]["QBXMLMsgsRs"]["CustomerQueryRs"]["CustomerRet"]

            # Handle scenarios where only a single record is returned in a response versus a list of records
            if not isinstance(records, list):
                records = [records]

            # Build each customer mutable object from the response data
            for record in records:
                # Translate the base customer fields
                customer: dict = CustomerMutable.extract_fields(record)

                # Translate customer address data
                if 'BillAddress' in record:
                    billing_address: dict = CustomerAddressMutable.extract_fields(record['BillAddress'])
                    customer['billing_address'] = CustomerAddressMutable(**billing_address)

                if 'ShipAddress' in record:
                    shipping_address: dict = CustomerAddressMutable.extract_fields(record['ShipAddress'])
                    customer['shipping_address'] = CustomerAddressMutable(**shipping_address)

                # Translate any ship-to addresses defined for the customer in Quickbooks
                if 'ShipToAddressList' in record and isinstance(record['ShipToAddressList'], list) \
                        and len(record['ShipToAddressList']):
                    customer['shipping_addresses'] = []

                    for address in record['ShipToAddressList']:
                        customer['shipping_addresses'].append(CustomerShippingAddressMutable(**address))

                data.append(CustomerMutable(**customer))

        return data

    @staticmethod
    def build_list_request(request_id: int = 1, iterator_id: str or None = None):
        from lxml import etree
        from src.qbsync.app import app

        attributes = CustomerApi.get_base_attributes(requestID=str(request_id))

        if not isinstance(iterator_id, str) or not len(iterator_id):
            attributes['iterator'] = "Start"
        else:
            attributes['iterator'] = "Continue"
            attributes['iteratorID'] = iterator_id

        # Create a Quickbooks request for the QBWC SOAP interface
        root = CustomerApi.build_qbxml_root()
        request = CustomerApi.build_qbxml_request(root=root)

        # Augment the SOAP request to query Quickbooks customer records
        query = etree.SubElement(request, 'CustomerQueryRq', attributes)

        # Add a maximum record limit to the request
        limit = etree.SubElement(query, 'MaxReturned')

        # Set the maximum record limit to the configured download page_size setting of the customer API
        limit.text = str(app.config['defaults']['api']['customers']['download']['page_size'])

        # Build the entire element tree for the SOAP request
        tree = CustomerApi.build_qbxml_tree(root=root)

        return tree
