import enums
from commands import m_command, m_message
import logging

from commands.m_command import command

logger = logging.getLogger(__name__)


class end_test_command(command):
    def __init__(self):
        command.__init__(self)
        self.response = None
        self.command_id = m_message.COMMAND_ID['EndTest']
        logger.info('%s COMMAND CREATE ', m_message.ID_TO_COMMAND[self.command_id])

    def write_data(self):
        command.write_data(self)

        return []
