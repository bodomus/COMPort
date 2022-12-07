import logging
from commands.m_finite_ramp_safe_duration_command import *
from Utilities import temp_converter, converters
from commands import m_message, m_command

logger = logging.getLogger(__name__)


class finite_ramp_by_time_command(finite_ramp_safe_duration_command):
    USE_TIME_MARK_BIT = 3

    def __init__(self):
        finite_ramp_safe_duration_command.__init__(self)
        self.response = None
        self.command_id = m_message.COMMAND_ID['FiniteRampByTime']
        logging.info('%s COMMAND CREATE ', m_message.ID_TO_COMMAND[self.command_id])
        self.m_isUseTimeMark = False

    def write_data(self):
        """
        :return: count bytes was written in buffer
        """
        # need testing
        m_command.command.write_data(self)
        position = m_command.LENGTH_EXTRA_DATA_COMMAND
        # write temperature
        temp = temp_converter.pc2tcu(self.m_temperature)
        self.command_array[position] = temp
        position += 2
        self.command_array[position] = self.m_time
        position += 4

        # options_byte
        options_byte = 0
        converters.set_bit(options_byte, self.WAIT_TRIGGER_BIT, self.m_isWaitForTrigger)
        converters.set_bit(options_byte, self.PEAK_DETECT_BIT, self.m_isPeakDetect)
        converters.set_bit(options_byte, self.CREATE_TIME_MARK_BIT, self.m_isCreateTimeMark)
        converters.set_bit(options_byte, self.USE_TIME_MARK_BIT, self.m_isUseTimeMark)
        converters.set_bit(options_byte, self.USE_DYNAMIC_FACTOR, self.m_isDynamicFactor)
        converters.set_bit(options_byte, self.ALLOW_EMPTY_BUFFER_BIT, self.m_isAllowEmptyBuffer)
        converters.set_bit(options_byte, self.IGNORE_KD_PID_PARAMETER_BIT, self.m_ignoreKdPidParameter)
        if self.m_allowSafeDurationOffset is not None:
            converters.set_bit(options_byte, self.ALLOW_SAFE_DURATION_OFFSET, self.m_allowSafeDurationOffset)
        self.command_array[position] = options_byte
        position += 1

        # stop_condition_byte
        stop_condition_byte = 0
        converters.set_bit(stop_condition_byte, self.STOP_ON_YES_BIT, self.m_isStopOnResponseUnitYes)
        converters.set_bit(stop_condition_byte, self.STOP_ON_NO_BIT, self.m_isStopOnResponseUnitNo)
        self.command_array[position] = stop_condition_byte
        position += 1

        # m_conditionEventsLength
        self.command_array[position] = self.m_conditionEventsLength
        position += 1

        return position - m_command.LENGTH_EXTRA_DATA_COMMAND
