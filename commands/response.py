import m_message

ACKCODE = {
    'Ok': 0,
    'UnsupportedCommand': 1,
    'WrongCRC': 2,
    'IllegalParameter': 3,
    'IllegalState': 4,
    'ThermodeDisabled': 5,
    'IllegalCommandSequence': 6,
    'BufferFull': 7,
    'NoDataExists': 8,
    'DataAlreadyExists': 9,
    'Fail': 10,  # Error during process command
    'WrongFlashAddress': 11,  # Error during process command
    'WrongSize': 12,  # Error during process command
    'Undefined': 255
}


class response(m_message.message):
    def __init__(self, command_id=None):
        m_message.message.__init__(self)
        self.command_ack_code = None

    def read_data(self, buffer):
        """
        read data from byte array to self
        :return:
        """
        pass
