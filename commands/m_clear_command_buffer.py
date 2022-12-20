import enums
from commands import m_command, m_message
import logging

from commands.m_command import command

logger = logging.getLogger(__name__)


# TODO Need Testing
class clear_command_buffer_command(command):
    def __init__(self):
        command.__init__(self)
        self.response = None
        self.command_id = enums.COMMAND_ID.ClearCommandBuffer
        logger.info('%s COMMAND CREATE ', str(self.command_id))

    def write_data(self):

        return command.write_data(self)

    def send_message(self):
        # command.send_message(self)
        logger.info(str(self))

    def __str__(self):
        return f'\t{command.__str__(self)}'
