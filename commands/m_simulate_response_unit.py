import enums
from Utilities import converters
from commands import m_command, m_message
import logging

from commands.m_command import command

logger = logging.getLogger(__name__)


class simulate_unit_response_command(command):
    BIT_YES = 0
    BIT_NO = 1

    def __init__(self):
        command.__init__(self)
        self.response = None
        self.m_isYesPressed = False
        self.m_isNoPressed = False
        self.command_id = m_message.COMMAND_ID['SimulateResponseUnit']
        logger.info('%s COMMAND CREATE ', m_message.ID_TO_COMMAND[self.command_id])

    def write_data(self):
        command.write_data(self)
        extra_data = [0x00]
        options_byte = 0

        options_byte = converters.set_bit(options_byte, self.BIT_YES, self.m_isYesPressed)
        options_byte = converters.set_bit(options_byte, self.BIT_NO, self.m_isNoPressed)
        extra_data[0] = options_byte

        return extra_data

    # Path: commands\m_run_test.py
    def __str__(self):
        command.send_message()
        logger.info(f'\tSimulateUnitResponse: was send to device')
