import enums
from commands import m_command, m_message
import logging

from commands.m_command import command

logger = logging.getLogger(__name__)


class set_TCU_state_command(command):
    def __init__(self):
        command.__init__(self)
        self.m_state = enums.SystemState['SafeMode']
        self.m_runSelfTest = True
        self.response = None
        self.command_id = m_message.COMMAND_ID['SetTcuState']
        logger.info('%s COMMAND CREATE ', m_message.ID_TO_COMMAND[self.command_id])

    def write_data(self):
        command.write_data(self)
        extra_data = [0x00] * 2
        extra_data[0] = self.m_state
        extra_data[1] = 1 if self.m_runSelfTest else 0

        return extra_data

