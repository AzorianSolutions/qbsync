from loguru import logger
from lxml.ElementInclude import etree


class BaseApi:
    DATA_TYPE: str or None = None
    _queue: list or None = None

    @staticmethod
    def build_list() -> list:
        return []

    @staticmethod
    def build_qbxml_root():
        from lxml import etree
        root = etree.Element("QBXML")
        root.addprevious(etree.ProcessingInstruction("qbxml", "version=\"8.0\""))
        return root

    @staticmethod
    def build_qbxml_tree(root) -> etree:
        from lxml import etree
        tree = etree.ElementTree(root)
        return etree.tostring(tree, xml_declaration=True, encoding='UTF-8')

    @classmethod
    def build_qbxml_request(cls, root=None):
        from lxml import etree

        # Automatically populate the root keyword argument if not of the proper type
        if root is None:
            root = cls.build_qbxml_root()

        return etree.SubElement(root, 'QBXMLMsgsRq', {'onError': 'stopOnError'})

    @staticmethod
    def get_base_attributes(**kwargs) -> dict:
        return {**kwargs}

    @classmethod
    def get_queue(cls) -> list or None:
        return cls._queue

    @classmethod
    def empty_queue(cls):
        cls._download_queue = None

    @staticmethod
    def queue_request(request: str, callback, request_id: str or None = None):
        from src.qbsync.request_manager import manager
        manager.queue_request({'request': request, 'request_id': request_id, 'callback': callback})

    @classmethod
    def queue_response(cls, response: str):
        if not isinstance(cls._queue, list):
            cls._queue = []
        cls._queue.append(response)

    @classmethod
    def save_queue(cls, data_type: str) -> bool:
        import csv
        import json
        import os
        import yaml
        from spnexus.utils.serialization import MutableJSONEncoder
        from src.qbsync.app import app

        if data_type not in app.config['defaults']['export']['types']:
            logger.error(f'Could not save download queue because an invalid data type was given: {data_type}')
            return False

        conf = app.config['defaults']['export']
        formats = conf['types'][data_type]
        export_path = f'{app.path}/{conf["path"]}'

        if export_path[-1] == '/':
            export_path = export_path[:-1]

        # Abort processing if the download queue is invalid or empty
        if not isinstance(cls.get_queue(), list) or not len(cls.get_queue()):
            return False

        data: list = cls.build_list()

        for export in formats:
            if export['format'] not in ['csv', 'json', 'yaml']:
                logger.warning(f'The export named "{export["name"]}" has an invalid format defined: {export["format"]}')
                continue

            file_path = f'{export_path}/{export["name"]}'
            file_contents: str = ''

            if os.path.exists(file_path) and not os.access(file_path, os.W_OK):
                logger.error(f'Could not export {data_type} data in {export["format"]} format. Destination path is'
                             + f' not writable: {file_path}')
                continue

            if export['format'] == 'csv':
                # Build a process that creates a series of CSV files with run-time generated linking IDs to connect
                # data relationships across files.
                file_contents = 'FEATURE_NOT_IMPLEMENTED'
                pass

            if export['format'] == 'json':
                file_contents = json.dumps(data, cls=MutableJSONEncoder)

            if export['format'] == 'yaml':
                file_contents = yaml.dump(data)

            # There is planned support for direct data injection into MySQL, PgSQL, and SQLite
            # including support for in-place updates to existing records

            with open(file_path, 'w') as f:
                f.write(file_contents)
                f.close()

            logger.info(f'Exported {data_type} data in {export["format"]} format to {file_path}.')

        return True
