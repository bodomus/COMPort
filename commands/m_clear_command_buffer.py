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
        self.command_id = m_message.COMMAND_ID['ClearCommandBuffer']
        logger.info('%s COMMAND CREATE ', m_message.ID_TO_COMMAND[self.command_id])

    def write_data(self):

        return command.write_data(self)
