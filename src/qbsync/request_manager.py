import uuid
from loguru import logger


class RequestManager:
    queue: list

    def __init__(self, queue: list or None = None):
        self.queue = queue
        if not isinstance(self.queue, list):
            self.queue = []

    def get_next_request(self) -> dict or None:
        if isinstance(self.queue, list) and len(self.queue):
            return self.queue[0]
        return None

    def get_current_request(self, request_id) -> str or bool:
        if not isinstance(self.queue, list) or not len(self.queue):
            logger.warning(f'There are no queue items for the request {request_id}.')
            return False

        if request_id != (queue_request_id := self.queue[0]['request_id']):
            logger.error(f'The given request ID {request_id} did not match the current queue item request ID'
                         + f' {queue_request_id}.')
            return False

        return self.queue[0]['request']

    def queue_request(self, msg):
        item = {
            **{
                'request_id': str(uuid.uuid1()),
                'update_pause': 0,
                'minimum_update': 60,
                'minimum_run_interval': 30,
            },
            **msg
        }

        if item['request_id'] is None:
            item['request_id'] = str(uuid.uuid1())

        self.queue.append(item)

    def handle_response(self, request_id, response):
        if isinstance(self.queue, list) and len(self.queue):
            if request_id != (queue_request_id := self.queue[0]['request_id']):
                logger.error(f'The given request ID {request_id} did not match the current queue item request ID'
                             + f' {queue_request_id}.')
                return False

            callback = None
            if 'callback' in self.queue[0]:
                callback = self.queue[0]['callback']

            self.queue.pop(0)

            if hasattr(callback, '__call__'):
                logger.debug(f'Executing response callback for request {request_id}.')
                return callback(request_id, response)
            else:
                logger.debug(f'Skipping response callback execution. No callback defined for request {request_id}.')

            return True


manager = RequestManager()
