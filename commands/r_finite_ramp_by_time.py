from Utilities import converters, temp_converter
from commands.m_finite_ramp_safe_duration_command import finite_ramp_safe_duration_command
# from commands.m_finite_ramp_safe_duration_command import finite_ramp_safe_duration_command
from commands.m_message import message
from commands.response import response
import logging

logger = logging.getLogger(__name__)


class finite_ramp_by_time_response(finite_ramp_safe_duration_command):
    USE_TIME_MARK_BIT = 3

    def __init__(self):
        finite_ramp_safe_duration_command.__init__(self)
        self.m_isUseTimeMark = False

    def read_data(self, buffer, start_position=0):
        count = response.read_data(buffer, start_position)
        temperature = converters.to_int_16(buffer, start_position)
        start_position += 2
        self.m_temperature = temp_converter.tcu2pc(temperature)

        time = converters.to_uint_32(buffer, start_position)
        start_position += 4
        self.m_time = time

        optionsByte = buffer[start_position]
        start_position += 1

        self.m_isWaitForTrigger = converters.get_bit(optionsByte, self.WAIT_TRIGGER_BIT)
        self.m_isPeakDetect = converters.get_bit(optionsByte, self.PEAK_DETECT_BIT)
        self.m_isCreateTimeMark = converters.get_bit(optionsByte, self.CREATE_TIME_MARK_BIT)
        self.m_isUseTimeMark = converters.get_bit(optionsByte, self.USE_TIME_MARK_BIT)
        self.m_isDynamicFactor = converters.get_bit(optionsByte, self.USE_DYNAMIC_FACTOR)
        self.m_isAllowEmptyBuffer = converters.get_bit(optionsByte, self.ALLOW_EMPTY_BUFFER_BIT)
        self.m_ignoreKdPidParameter = converters.get_bit(optionsByte, self.IGNORE_KD_PID_PARAMETER_BIT)
        stopConditionsByte = buffer[start_position]
        start_position += 1
        self.m_isStopOnResponseUnitYes = converters.get_bit(stopConditionsByte, self.STOP_ON_YES_BIT)
        self.m_isStopOnResponseUnitNo = converters.get_bit(stopConditionsByte, self.STOP_ON_NO_BIT)
        # TODO ConditionEventsCount = reader.ReadByte();

    def __str__(self):
        base = str(response.__str__(self))

        info = "{0}\nm_isWaitForTrigger: {1}\nm_isPeakDetect: {2}\n" \
               "m_isCreateTimeMark: {3}\n" \
               "m_isUseTimeMark: {4}\n" \
               "m_isDynamicFactor: {5}\n" \
               "m_isAllowEmptyBuffer: {6}\n" \
               "m_ignoreKdPidParameter: {7}\n" \
               "m_isStopOnResponseUnitYes: {8}\n" \
               "m_isStopOnResponseUnitNo: {9}\n" \
            .format(
            base,
            self.m_isWaitForTrigger,
            self.m_isPeakDetect,
            self.m_isCreateTimeMark,
            self.m_isUseTimeMark,
            self.m_isDynamicFactor,
            self.m_isAllowEmptyBuffer,
            self.m_ignoreKdPidParameter,
            self.m_isStopOnResponseUnitYes,
            self.m_isStopOnResponseUnitNo
        )
        return info

    def response_message(self):
        logger.info(f'Response finite_ramp_by_time_response from device:::version {self.m_temperature}')
