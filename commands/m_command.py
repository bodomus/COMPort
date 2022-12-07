import crc8
import logging
from Utilities import converters
from commands import m_message
import ack_code

CRC_INDEX = 0
LENGTH_INDEX = 1
LENGTH_ID = LENGTH_INDEX + 2
LENGTH_TOKEN = LENGTH_ID + 1
LENGTH_TAG = LENGTH_TOKEN + 4
LENGTH_EXTRA_DATA = LENGTH_TAG + 1
# for response
LENGTH_ACK_CODE = LENGTH_TAG + 1

DEVICE_TAG = {
    'Master': 0,
    'Slave': 1
}


class command(m_message.message):

    def __init__(self):
        # super(command, self).__init__()
        m_message.message.__init__(self)
        self.response = None
        self.command_id = m_message.COMMAND_ID['GetVersion']
        logging.info('%s COMMAND CREATE ', "GetVersion")

    def to_bytes(self):
        """
            create bytes from command
            :param command: object that need convert to bytes
        """
        if self.command_id == m_message.COMMAND_ID['Undefined']:
            raise ValueError("Invalid command id")
        self.command_array = [0x00] * m_message.MAX_LENGTH
        self.command_array[LENGTH_ID] = self.command_id
        if self.command_token is not None:
            tok = converters.get_bytes32(self.command_token)
            self.command_array[LENGTH_TOKEN] = tok[3]
            self.command_array[LENGTH_TOKEN + 1] = tok[2]
            self.command_array[LENGTH_TOKEN + 2] = tok[1]
            self.command_array[LENGTH_TOKEN + 3] = tok[0]
        self.command_array[LENGTH_TAG] = 0 if self.command_tag is None else self.command_tag
        write_len = self.write_data()
        # write command length
        command_length = LENGTH_TAG + write_len
        array_length = converters.get_bytes16(command_length)
        self.command_array[LENGTH_INDEX] = array_length[1]  #
        self.command_array[LENGTH_INDEX + 1] = array_length[0]
        # write_data

        # write crc8
        crc = crc8.calculate(self.command_array, CRC_INDEX + 1, command_length)
        self.command_array[CRC_INDEX] = crc

    def write_data(self):
        """
        :param buffer: bytes array of command
        :return: count bytes was writen in buffer
        """
        return 0
        # TODO need implementation in subclass

    def from_bytes(self, bytes):
        """
            Realizaation for TSA3 only
            asdasda
            :param bytes:
        """
        length = converters.to_int_16(bytes, LENGTH_INDEX)
        super().command_id = m_message.ID_TO_COMMAND[bytes[LENGTH_ID]]
        super().command_token = bytes[LENGTH_TOKEN]
        super().command_tag = bytes[LENGTH_TAG]

    def receive_response(self, header_buffer, body_buffer):
        """
        :param header_buffer: list of 4 bytes represent header response
        :param body_buffer: body response
        :return:
        """
        command_length = converters.to_u_int_16_ex(header_buffer, LENGTH_INDEX) - len(header_buffer) + 1
        buffer = list(header_buffer)
        buffer.extend(body_buffer[0: command_length])
        self.get_message(buffer)

    def get_message(self, buffer):
        """
        :type list
        :param buffer
        :return object: response
        :Date: 2022-11-30
        :Version: 1
        :Authors: bodomus@gmail.com
        """
        crc = buffer[CRC_INDEX]
        length = converters.to_uint_16(buffer, LENGTH_INDEX)
        if length + 1 > len(buffer):
            raise ValueError("Invalid length of input buffer")
        crcCalculated = crc8.calculate(buffer, CRC_INDEX + 1, length)
        if crc8 != crcCalculated:
            raise ValueError("Invalid crc code")
        self.command_id = buffer[LENGTH_ID]
        #
        # TODO create response command
        self.create_response(buffer)

    def create_response(self, buffer) -> object:
        """
            Вызывается когда получен ответ от железа для конвертации байтов в команду
            :type list
            :param buffer
            :return object: response
            :Date: 2022-11-30
            :Version: 1
            :Authors: bodomus@gmail.com
        """
        length = converters.to_uint_16(buffer, LENGTH_INDEX)
        self.response = command()
        self.response.command_id = buffer[LENGTH_ID]
        self.response.command_token = converters.to_uint_32(buffer, LENGTH_TOKEN)
        self.response.command_tag = buffer[LENGTH_TAG]
        self.response.command_ack_code = buffer[LENGTH_ACK_CODE]
        # if self.response.command_ack_code == ack_code.ACKCODE['Ok']:
        # TODO need complete
