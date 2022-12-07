#from response import *
from Utilities import converters
from commands.response import response
import logging
#from m_command import *

logger = logging.getLogger(__name__)


class get_version_response(response):
    def __init__(self):
        response.__init__(self)
        self.m_version = None

    def read_data(self, buffer, start_position=0):
        count = response.read_data(buffer, start_position)
        self.m_version = converters.to_string(buffer, start_position)

    def response_message(self):
        response.response_message(self)
        logger.info(f'Response from device:::version {self.m_version}')

