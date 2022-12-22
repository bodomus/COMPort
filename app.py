from datetime import datetime
import enums
from commands import m_command
from commands.erase_error_command import erase_error_command
from commands.m_clear_command_buffer import clear_command_buffer_command
from commands.m_enable_termode import enable_termode_command
from commands.m_end_test_command import end_test_command
from commands.m_finite_ramp_by_temperature_command import finite_ramp_by_temperature_command
from commands.m_finite_ramp_by_time_command import finite_ramp_by_time_command
from commands.m_get_active_thermode import get_active_thermode_command
from commands.m_get_error_command import get_errors_command
from commands.m_getstatusTCU_command import get_status_TCU_command
from commands.m_run_test import run_test_command
from commands.m_simulate_response_unit import simulate_unit_response_command
from commands.m_stop_test_command import stop_test_command
from input_commands import *
import switch_command
from connector import connector
import time
from commands import m_getVersion_command, m_set_TCU_state

INTERVAL = 50  # ms


class app:
    def __init__(self):
        self.m_waiting_self_test = None
        self.ser = None
        self.current_time = self.getseconds(in_millisecondes=True)
        self.token = 0
        self.disable_get_status = False
        self.input_commands = input_commands()
        self.input_commands.load_commands("commands.json")
        self.waiting_self_test = False
    def initialize(self):
        con = connector("preferences.json")
        self.ser = con.get_com_port()

    def finalize(self):
        if self.ser is not None and self.ser.is_open:
            self.ser.close()

    def getseconds(self, in_millisecondes=False):
        now = datetime.now()
        if in_millisecondes:
            return round((now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()) * 1000
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

    def get_errors(self, token):
        """
        create command get errors
        :param token: current command token
        :return: command get status TCU
        """
        com = get_errors_command()
        com.command_token = token
        com.send_message()
        com.to_bytes()
        return com

    def command_builder(self, command_id, token, data):
        """
        :param command_id:
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
            command = end_test_command()
        if command_id == enums.COMMAND_ID.StopTest.value:
            command = stop_test_command()
        if command_id == enums.COMMAND_ID.FiniteRampByTime.value:
            command = finite_ramp_by_time_command()
        if command_id == enums.COMMAND_ID.FiniteRampByTemperature.value:
            command = finite_ramp_by_temperature_command()
        if command_id == enums.COMMAND_ID.SimulateResponseUnit.value:
            command = simulate_unit_response_command()
        if command_id == enums.COMMAND_ID.GetErrors.value:
            command = get_errors_command()
        if command_id == enums.COMMAND_ID.EraseErrors.value:
            command = erase_error_command()

        command.build_command(data)
        command.command_token = token
        command.send_message()
        command.to_bytes()
        return command

    def run(self):
        current_command_index = 0
        com = None
        self.initialize()
        try:
            while 1:
                self.token += 1
                t = self.getseconds(in_millisecondes=True)
                if len(self.input_commands.commands) == current_command_index:
                    self.finish()
                    return
                # if self.current_time + 50 < t:
                #     com = self.get_status_tcu(self.token)
                # else:
                data = self.input_commands.commands[current_command_index]
                com = self.command_builder(data["commandId"], self.token, data)
                if com.command_id == enums.COMMAND_ID.SetTcuState and com.m_state == enums.SystemState.RestMode:
                    self.waiting_self_test = True
                current_command_index += 1

                if not self.ser.is_open:
                    self.ser.open()
                self.ser.reset_input_buffer()
                self.ser.reset_output_buffer()
                time.sleep(0.5)
                send_length = self.ser.write(com.command_array)
                self.ser.flush()

                header = self.ser.read(4)
                command_length = com.header_length_from_bytes(header)
                while self.ser.in_waiting:
                    data = self.ser.read(command_length)
                    com.receive_response(header, data)
                    com.response.response_message()
                    if com.command_id == enums.COMMAND_ID.GetStatusTCU and self.waiting_self_test:
                        time.sleep(12)
                        if com.response.get_state() != enums.SystemState.RestMode:
                            self.input_commands.commands.insert(current_command_index, {"commandId": enums.COMMAND_ID.GetStatusTCU.value})
                            logger.info("Repeat get status TCU")
                        else:
                            self.m_waiting_self_test = False


                        # if com.response.m_isError:
                        #     self.input_commands.commands.insert(current_command_index,
                        #                                         {"commandId": enums.COMMAND_ID.EraseErrors.value})
                        #     self.input_commands.commands.insert(current_command_index,
                        #                                         {"commandId": enums.COMMAND_ID.GetErrors.value})

                self.current_time = t

                self.ser.close()
        except Exception as e:
            logger.error('Failed: ' + str(e))
        finally:
            self.finalize()


def creator():
    switch = switch_command()
    switch.get_command('GetCommandTCU')


if __name__ == '__main__':
    import logging.config

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.DEBUG)
    # logging.basicConfig(filename="log.log",
    #                     filemode='a',
    #                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    #                     datefmt='%H:%M:%S',
    #                     level=logging.DEBUG)
    logging.info('start app module.')
    app = app()
    start_time = app.getseconds(in_millisecondes=True)
    app.run()
    end_time = app.getseconds(in_millisecondes=True)
    logger.info(f"Complete. Total running time {round(end_time - start_time)} seconds")
