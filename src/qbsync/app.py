from argparse import Namespace
from flask import Flask
from loguru import logger
from multiprocessing import Process, Queue
from wsgiref.simple_server import WSGIServer


class QBSyncApp:
    path: str
    args: Namespace
    config: dict
    users: dict
    requests: Queue
    responses: Queue
    soap_process: Process
    http_process: Process
    soap_server: WSGIServer
    http_server: Flask

    def __init__(self, app_path: str, args: Namespace):
        logger.debug(f'Initializing QBSync application.')

        if app_path[-1] == '/':
            app_path = app_path[:-1]

        # Setup application resources
        self.path = app_path
        self.args = args
        self.requests = Queue()
        self.responses = Queue()

        # Load application configuration
        self.load_yaml(prop_name='config')

        # Load application users
        self.load_yaml(prop_name='users')

        # Initialize network servers
        self.soap_process = Process(target=self.soap_server_start, args=(self.requests, self.responses))
        self.http_process = Process(target=self.http_server_start, args=(self.requests, self.responses))

    def run(self):
        logger.debug(f'Starting QBSync SOAP service.')
        self.soap_process.start()
        logger.debug(f'Starting QBSync HTTP service.')
        self.http_process.start()

    def load_yaml(self, prop_name: str) -> bool:
        import os
        from yaml import full_load

        config_path = None

        if prop_name == 'config':
            config_path = self.args.config_file

        if prop_name == 'users':
            config_path = self.config['defaults']['auth']['users_path']

        if not isinstance(config_path, str):
            logger.error(f'Invalid YAML file type given: {prop_name}.')
            return False

        # Clean-up relative configuration paths to always start from the application root path
        if config_path[0] != '/':
            config_path = f'{self.path}/{config_path}'

        config_path = os.path.realpath(config_path)

        logger.debug(f'Loading QBSync YAML file for {prop_name} from {config_path}.')

        if not os.path.exists(config_path):
            logger.critical(f'YAML file for {prop_name} does not exist at {config_path}!')
            return False

        if not os.access(config_path, os.R_OK):
            logger.critical(f'YAML file for {prop_name} not readable at {config_path}!')
            return False

        with open(config_path, 'r') as f:
            setattr(self, prop_name, full_load(f))
            f.close()

        return True

    def save_yaml(self, prop_name: str) -> bool:
        import os
        import yaml

        config_path = None

        if prop_name == 'config':
            config_path = self.args.config_file

        if prop_name == 'users':
            config_path = self.config['defaults']['auth']['users_path']

        if not isinstance(config_path, str):
            logger.error(f'Invalid YAML file type given: {prop_name}.')
            return False

        # Clean-up relative configuration paths to always start from the application root path
        if config_path[0] != '/':
            config_path = f'{self.path}/{config_path}'

        config_path = os.path.realpath(config_path)

        logger.debug(f'Saving QBSync YAML file for {prop_name} to {config_path}.')

        if not os.access(config_path, os.W_OK):
            logger.critical(f'YAML file for {prop_name} not writable at {config_path}!')
            return False

        with open(config_path, 'w') as f:
            yaml.dump(self.users, f)
            f.close()

        return True

    def soap_server_start(self, request_queue, response_queue):
        from spyne import Application
        from spyne.protocol.soap import Soap11
        from spyne.server.wsgi import WsgiApplication
        from wsgiref.simple_server import make_server
        from src.qbsync.services.quickbooks import QuickbooksService
        conf = self.config['defaults']['servers']['soap']

        spyne_app = Application([QuickbooksService], 'http://developer.intuit.com/',
                                in_protocol=Soap11(validator='lxml'),
                                out_protocol=Soap11())

        wsgi_app = WsgiApplication(spyne_app)

        self.soap_server = make_server(conf['host'], conf['port'], wsgi_app)
        self.soap_server.serve_forever()

    def http_server_start(self, request_queue, response_queue):
        from src.qbsync.services.http import make_server
        conf = self.config['defaults']['servers']['http']
        self.http_server = make_server()
        self.http_server.config['requestQueue'] = request_queue
        self.http_server.config['responseQueue'] = response_queue
        self.http_server.run(host=conf['host'], port=conf['port'], debug=conf['debug'])


app: QBSyncApp
