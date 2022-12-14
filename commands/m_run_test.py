import enums
from commands import m_command, m_message
import logging

from commands.m_command import command

logger = logging.getLogger(__name__)


class run_test_command(command):
    def __init__(self):
        command.__init__(self)
        self.response = None
        self.m_isResetClock = True
        self.command_id = m_message.COMMAND_ID['RunTest']
        logger.info('%s COMMAND CREATE ', m_message.ID_TO_COMMAND[self.command_id])

    def write_data(self):
        command.write_data(self)
        extra_data = [0x00]
        extra_data[0] = 0x1 if self.m_isResetClock else 0x0

        return extra_data

    # Path: commands\m_run_test.py
    def __str__(self):
        command.send_message()
        logger.info(f'\truntest: was send to device')
        logger.info(f'\t\t: {self.m_isResetClock}')
