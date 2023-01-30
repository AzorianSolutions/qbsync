from loguru import logger
from src.qbsync.api.base import BaseApi


class InvoiceApi(BaseApi):
    DATA_TYPE = 'invoices'

    @staticmethod
    def download():
        logger.debug(f'Downloading Quickbooks invoice data.')

        # Clear any lingering records from the download queue
        InvoiceApi.empty_queue()

        # Set up first download request
        request = InvoiceApi.build_list_request()

        # Queue the download request
        InvoiceApi.queue_request(request=request, callback=InvoiceApi.receive_download)

    @staticmethod
    def receive_download(request_id: str or None, response: str or None):
        from lxml import etree

        if not isinstance(response, str) or not len(response.strip()):
            return

        # Queue the response for processing after downloading is complete
        InvoiceApi.queue_response(response)

        # Extract the total remaining records for the iterator from the response
        root = etree.fromstring(response)
        remaining_search = root.xpath('//InvoiceQueryRs/@iteratorRemainingCount')
        total_remaining: int = 0
        if isinstance(remaining_search, list) and len(remaining_search):
            total_remaining = int(remaining_search[0])

        logger.debug(f'Total Downloads Remaining: {total_remaining}')

        # Setup additional download request when the iterator has additional records
        if total_remaining:
            req_id = int(root.xpath('//InvoiceQueryRs/@requestID')[0]) + 1
            iterator_id = root.xpath('//InvoiceQueryRs/@iteratorID')[0]

            # Set up the download request
            request = InvoiceApi.build_list_request(request_id=req_id, iterator_id=iterator_id)

            # Queue the download request
            InvoiceApi.queue_request(request=request, callback=InvoiceApi.receive_download, request_id=request_id)

        # Process response data now that there are no remaining records to be downloaded
        else:
            InvoiceApi.save_queue(InvoiceApi.DATA_TYPE)

    @staticmethod
    def build_list() -> list:
        import xmltodict
        from src.qbsync.mutables.invoice import InvoiceMutable
        from src.qbsync.mutables.invoice_item import InvoiceItemMutable
        from src.qbsync.mutables.invoice_item_group import InvoiceItemGroupMutable
        from src.qbsync.mutables.customer_address import CustomerAddressMutable

        data: list = []

        # Process queued download responses sequentially
        for response in InvoiceApi.get_queue():
            doc = xmltodict.parse(response)

            if 'InvoiceRet' not in doc["QBXML"]["QBXMLMsgsRs"]["InvoiceQueryRs"]:
                continue

            records = doc["QBXML"]["QBXMLMsgsRs"]["InvoiceQueryRs"]["InvoiceRet"]

            # Handle scenarios where only a single record is returned in a response versus a list of records
            if not isinstance(records, list):
                records = [records]

            # Build each invoice mutable object from the response data
            for record in records:
                # Translate the base invoice fields
                invoice: dict = InvoiceMutable.extract_fields(record)

                # Translate customer address data
                if 'BillAddress' in record:
                    billing_address: dict = CustomerAddressMutable.extract_fields(record['BillAddress'])
                    invoice['billing_address'] = CustomerAddressMutable(**billing_address)

                if 'ShipAddress' in record:
                    shipping_address: dict = CustomerAddressMutable.extract_fields(record['ShipAddress'])
                    invoice['shipping_address'] = CustomerAddressMutable(**shipping_address)

                # Translate invoice line items and item groups
                if 'InvoiceLineRet' in record and isinstance(record['InvoiceLineRet'], list) \
                        and len(record['InvoiceLineRet']):
                    invoice['items'] = []

                    for line in record['InvoiceLineRet']:

                        if 'ItemRef' in line:
                            invoice_item: dict = InvoiceItemMutable.extract_fields(line)
                            invoice['items'].append(InvoiceItemMutable(**invoice_item))

                        elif 'ItemGroupRef' in line:
                            invoice_item_group: dict = InvoiceItemGroupMutable.extract_fields(line)
                            invoice_item_group['items'] = []

                            if 'InvoiceLineRet' in line:
                                lines = line['InvoiceLineRet']

                                if not isinstance(lines, list):
                                    lines = [lines]

                                for group_line in lines:
                                    invoice_item_group_item: dict = InvoiceItemMutable.extract_fields(group_line)
                                    invoice_item_group['items'].append(InvoiceItemMutable(**invoice_item_group_item))

                            invoice['items'].append(InvoiceItemGroupMutable(**invoice_item_group))

                data.append(InvoiceMutable(**invoice))

        return data

    @staticmethod
    def build_list_request(request_id: int = 1, iterator_id: str or None = None):
        from lxml import etree
        from src.qbsync.app import app

        attributes = InvoiceApi.get_base_attributes(requestID=str(request_id))

        if not isinstance(iterator_id, str) or not len(iterator_id):
            attributes['iterator'] = "Start"
        else:
            attributes['iterator'] = "Continue"
            attributes['iteratorID'] = iterator_id

        # Create a base request for the QBWC SOAP interface
        root = InvoiceApi.build_qbxml_root()
        msg = InvoiceApi.build_qbxml_request(root=root)

        # Augment the SOAP request to query Quickbooks invoice records
        irq = etree.SubElement(msg, 'InvoiceQueryRq', attributes)

        # Add a maximum record limit to the request based on the download page_size setting of the customer API
        mrt = etree.SubElement(irq, 'MaxReturned')
        mrt.text = str(app.config['defaults']['api']['invoices']['download']['page_size'])

        # Add a date range filter to the transaction date
        drf = etree.SubElement(irq, 'TxnDateRangeFilter')

        # drf_macro = etree.SubElement(drf, 'DateMacro')
        # drf_macro.text = str('LastMonth')

        drf_from = etree.SubElement(drf, 'FromTxnDate')
        drf_from.text = str('2023-01-01')

        drf_to = etree.SubElement(drf, 'ToTxnDate')
        drf_to.text = str('2023-01-01')

        # Add flag to include invoice line items in response
        ili = etree.SubElement(irq, 'IncludeLineItems')
        ili.text = 'true'

        # Build the entire element tree for the SOAP request
        return InvoiceApi.build_qbxml_tree(root=root)
