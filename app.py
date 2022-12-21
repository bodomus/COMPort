from datetime import datetime

import enums
from commands import m_command
from commands.m_clear_command_buffer import clear_command_buffer_command
from commands.m_enable_termode import enable_termode_command
from commands.m_finite_ramp_by_temperature_command import finite_ramp_by_temperature_command
from commands.m_finite_ramp_by_time_command import finite_ramp_by_time_command
from commands.m_get_active_thermode import get_active_thermode_command
from commands.m_getstatusTCU_command import get_status_TCU_command
from commands.m_run_test import run_test_command
from commands.m_simulate_response_unit import simulate_unit_response_command
from input_commands import *
import switch_command
from commands import m_message
from connector import connector
import time
from commands import m_getVersion_command, m_set_TCU_state

INTERVAL = 50  # ms


class app:
    def __init__(self):
        self.current_time = self.getseconds()
        self.token = 0
        self.input_commands = input_commands()
        self.input_commands.load_commands("commands.json")
        con = connector("preferences.json")
        self.ser = con.get_com_port()

    def getseconds(self):
        now = datetime.now()
        return round((now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds())

    def get_status_tcu(self, token):
        """
        create command get status TCU
        :param token: current command token
        :return: command get status TCU
        """
        com = get_status_TCU_command()
        com.command_token = token
        com.send_message()
        com.to_bytes()
        return com

    def command_builder(self, command_id, token, data):
        """
        :param token: token operation
        :param command: command for create
        :param data: data in json format with params
        :return:
        """
        command = None
        if command_id == enums.COMMAND_ID.SetTcuState.value:
            command = m_set_TCU_state.set_TCU_state_command()
        if command_id == enums.COMMAND_ID.GetVersion.value:
            command = m_getVersion_command.getVersion_command()
        if command_id == enums.COMMAND_ID.GetStatusTCU.value:
            command = get_status_TCU_command()
        if command_id == enums.COMMAND_ID.GetActiveThermode.value:
            command = get_active_thermode_command()
        if command_id == enums.COMMAND_ID.ClearCommandBuffer.value:
            command = clear_command_buffer_command()
        if command_id == enums.COMMAND_ID.RunTest.value:
            command = run_test_command()
        if command_id == enums.COMMAND_ID.EndTest.value:
            command = run_test_command()
        if command_id == enums.COMMAND_ID.StopTest.value:
            command = run_test_command()
        if command_id == enums.COMMAND_ID.FiniteRampByTime.value:
            command = finite_ramp_by_time_command()
        if command_id == enums.COMMAND_ID.FiniteRampByTemperature.value:
            command = finite_ramp_by_temperature_command()
        if command_id == enums.COMMAND_ID.SimulateResponseUnit.value:
            command = simulate_unit_response_command()
        if command_id == enums.COMMAND_ID.EnableThermode.value:
            command = enable_termode_command()

        command.build_command(data)
        command.command_token = token
        command.send_message()
        command.to_bytes()
        return command

    def run(self):

        # creator()
        current_command_index = 0
        com = None
        while 1:
            self.token += 1
            t = self.getseconds()
            # if self.current_time + 1 < t:
            #     self.current_time = t
            #     com = self.get_status_tcu(self.token)
            # else:
            if len(self.input_commands.commands) == current_command_index:
                logger.info("Complete")
                exit(0)
            data = self.input_commands.commands[current_command_index]
            com = self.command_builder(data["commandId"], self.token, data)
            current_command_index += 1

            time.sleep(1)
            if not self.ser.is_open:
                self.ser.open()

            send_length = self.ser.write(com.command_array)
            self.ser.flush()


            header = self.ser.read(4)
            command_length = com.header_length_from_bytes(header)
            while self.ser.in_waiting:
                data = self.ser.read(command_length)
                com.receive_response(header, data)
                com.response.response_message()


            self.ser.close()

            if not self.ser.is_open:
                print('port close')


def creator():
    switch = switch_command()
    switch.get_command('GetCommandTCU')


if __name__ == '__main__':
    import logging.config

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.DEBUG)
    logging.info('start app module.')
    app = app()
    app.run()
