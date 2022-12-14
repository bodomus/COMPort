import logging

from commands.m_command import command
from commands.m_finite_ramp_safe_duration_command import *
from Utilities import temp_converter, converters
from commands import m_message, m_command

logger = logging.getLogger(__name__)


class finite_ramp_by_temperature_command(finite_ramp_safe_duration_command):

    def __init__(self):
        finite_ramp_safe_duration_command.__init__(self)
        self.m_lowMargin = 0
        self.m_highMargin = 0
        self.response = None
        self.command_id = m_message.COMMAND_ID['FiniteRampByTemperature']
        logging.info('%s COMMAND CREATE ', m_message.ID_TO_COMMAND[self.command_id])

    def write_data(self):
        """
        :return: count bytes was written in buffer
        """
        # need testing
        extra_data = [0x00] * 13
        command.write_data(self)
        position = 0
        # write temperature
        temp = converters.get_bytes16(temp_converter.pc2tcu(self.m_temperature))
        extra_data[position] = temp[1]
        extra_data[position+1] = temp[0]
        position += 2

        low = converters.get_bytes16(temp_converter.pc2tcu(self.m_lowMargin))
        extra_data[position] = low[1]
        extra_data[position + 1] = low[0]
        position += 2

        high = converters.get_bytes16(temp_converter.pc2tcu(self.m_highMargin))
        extra_data[position] = high[1]
        extra_data[position + 1] = high[0]
        position += 2

        tok = converters.get_bytes32(self.m_time)
        extra_data[position] = tok[3]
        extra_data[position + 1] = tok[2]
        extra_data[position + 2] = tok[1]
        extra_data[position + 3] = tok[0]
        position += 4

        # options_byte
        options_byte = 0

        options_byte = converters.set_bit(options_byte, self.WAIT_TRIGGER_BIT, self.m_isWaitForTrigger)
        options_byte = converters.set_bit(options_byte, self.PEAK_DETECT_BIT, self.m_isPeakDetect)
        options_byte = converters.set_bit(options_byte, self.CREATE_TIME_MARK_BIT, self.m_isCreateTimeMark)
        options_byte = converters.set_bit(options_byte, self.USE_DYNAMIC_FACTOR, self.m_isDynamicFactor)
        options_byte = converters.set_bit(options_byte, self.ALLOW_EMPTY_BUFFER_BIT, self.m_isAllowEmptyBuffer)
        options_byte = converters.set_bit(options_byte, self.IGNORE_KD_PID_PARAMETER_BIT, self.m_ignoreKdPidParameter)

        if self.m_allowSafeDurationOffset is not None:
            options_byte = converters.set_bit(options_byte, self.ALLOW_SAFE_DURATION_OFFSET, self.m_allowSafeDurationOffset)
        extra_data[position] = options_byte
        position += 1

        # stop_condition_byte
        stop_condition_byte = 0
        stop_condition_byte = converters.set_bit(stop_condition_byte, self.STOP_ON_YES_BIT, self.m_isStopOnResponseUnitYes)
        stop_condition_byte = converters.set_bit(stop_condition_byte, self.STOP_ON_NO_BIT, self.m_isStopOnResponseUnitNo)
        extra_data[position] = stop_condition_byte
        position += 1

        # m_conditionEventsLength
        extra_data[position] = self.m_conditionEventsLength
        position += 1

        return extra_data

    def __str__(self):
        logger.info(f'\tfinite_ramp_by_temperature: was send to device')
        logger.info(f'\t\t: {self.m_temperature}')
        logger.info(f'\t\t: {self.m_time}')
