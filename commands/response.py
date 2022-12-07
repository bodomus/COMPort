import logging
from commands.m_message import message, ID_TO_COMMAND
from enums import ID_TO_ACKCODE

logger = logging.getLogger(__name__)

class response(message):
    def __init__(self, command_id=None):
        message.__init__(self)
        self.command_ack_code = None

    def read_data(self, buffer, start_position=0):
        """
        read data from byte array to self
        :return:
        """
        pass

    def response_message(self):
        """
        create response message
        :return:
        """
        logger.info(f'Response from device:::command {ID_TO_COMMAND[self.command_id]}:::ack code {ID_TO_ACKCODE[self.command_ack_code]}:::')

