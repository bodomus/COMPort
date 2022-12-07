from commands.m_command import *


class finiteRampByTime_command(command):
    def __init__(self):
        # super(command, self).__init__()
        message.__init__(self)
        self.response = None
        self.command_id = COMMAND_ID['FiniteRampByTime']
        logging.info('%s COMMAND CREATE ', ID_TO_COMMAND[self.command_id])

    def write_data(self):
        command.write_data(self)
        optionsByte = 0
        converters.set_bit()

        """
        :return: count bytes was writen in buffer
        """
        return 0
