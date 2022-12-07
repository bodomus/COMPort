from commands import m_command, m_message
import logging

from commands.m_command import command

logger = logging.getLogger(__name__)


class getVersion_command(command):
    def __init__(self):
        # super(command, self).__init__()
        command.__init__(self)
        self.response = None
        self.command_id = m_message.COMMAND_ID['GetVersion']
        logger.info('%s COMMAND CREATE ', m_message.ID_TO_COMMAND[self.command_id])