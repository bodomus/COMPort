from commands import m_command, m_message
import logging

logger = logging.getLogger(__name__)


class get_status_TCU_command(m_command.command):
    def __init__(self):
        # super(command, self).__init__()
        m_command.command.__init__(self)
        self.response = None
        self.command_id = m_message.COMMAND_ID['GetStatusTCU']
        logger.info('%s COMMAND CREATE ', m_message.ID_TO_COMMAND[self.command_id])