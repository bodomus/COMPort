import enums
from commands import m_command, m_message
import logging

from commands.m_command import command

logger = logging.getLogger(__name__)


class get_active_thermode_command(command):
    def __init__(self):
        command.__init__(self)
        self.m_thermodeId = 0
        self.response = None
        self.command_id = enums.COMMAND_ID.GetActiveThermode
        logger.info('%s COMMAND CREATE ', str(self.command_id))

    def write_data(self):
        command.write_data(self)
        extra_data = [0x00]
        extra_data[0] = self.m_thermodeId

        return extra_data

    def build_command(self, data):
        """
        build parameters from json file
        :param data: instance of command from json file from him parameters
        :return:
        """
        if 'm_thermodeId' in data.keys():
            self.m_thermodeId = data['m_thermodeId']

    def send_message(self):
        # command.send_message(self)
        logger.info(f'{str(self)}')

    def __str__(self):
        return f'\t{command.__str__(self)}'
