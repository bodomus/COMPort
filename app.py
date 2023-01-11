import time
from datetime import datetime
import enums
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
from connector import connector
from commands import m_getVersion_command, m_set_TCU_state
from state_machine import state_machine

INTERVAL = 50  # ms


class app:
    def __init__(self):
        self.sm = None
        self.ser = None
        self.current_time = self.getmseconds()
        self.token = 0
        self.disable_get_status = False
        self.input_commands = input_commands()
        self.input_commands.load_commands("commands.json")
        self.waiting_self_test = False
        self.current_state = enums.SystemState.SafeMode
        self.run_count = 0

    def initialize(self):
        con = connector("preferences.json")
        self.ser = con.get_com_port()
        self.sm = state_machine(self.ser)

    def finalize(self):
        if self.ser is not None and self.ser.is_open:
            self.ser.close()

    def read_comport_preferences(data):
        """
        read comport preferences
        :return:
        """
        pass

    def getmseconds(self):
        return round(time.time() * 1000)
        # now = datetime.now()
        # if in_millisecondes:
        #     return (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds() * 1000
        # return round((now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds())

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
        elif command_id == enums.COMMAND_ID.GetVersion.value:
            command = m_getVersion_command.getVersion_command()
        elif command_id == enums.COMMAND_ID.GetStatusTCU.value:
            command = get_status_TCU_command()
        elif command_id == enums.COMMAND_ID.GetActiveThermode.value:
            command = get_active_thermode_command()
        elif command_id == enums.COMMAND_ID.ClearCommandBuffer.value:
            command = clear_command_buffer_command()
        elif command_id == enums.COMMAND_ID.RunTest.value:
            command = run_test_command()
        elif command_id == enums.COMMAND_ID.EndTest.value:
            command = end_test_command()
        elif command_id == enums.COMMAND_ID.StopTest.value:
            command = stop_test_command()
        elif command_id == enums.COMMAND_ID.FiniteRampByTime.value:
            command = finite_ramp_by_time_command()
        elif command_id == enums.COMMAND_ID.FiniteRampByTemperature.value:
            command = finite_ramp_by_temperature_command()
        elif command_id == enums.COMMAND_ID.SimulateResponseUnit.value:
            command = simulate_unit_response_command()
        elif command_id == enums.COMMAND_ID.GetErrors.value:
            command = get_errors_command()
        elif command_id == enums.COMMAND_ID.EraseErrors.value:
            command = erase_error_command()
        elif command_id == enums.COMMAND_ID.EnableThermode.value:
            command = enable_termode_command()

        command.build_command(data)
        command.command_token = token
        command.send_message()
        command.to_bytes()
        return command

    def exec_test(self):
        current_command_index = 0
        com = None
        self.initialize()
        self.current_time = self.getmseconds()
        try:
            while 1:
                self.token += 1
                t = self.getmseconds()
                if len(self.input_commands.commands) == current_command_index or self.token == -1:
                    return
                logger.info("CURRENT command index: {0}".format(current_command_index))
                logger.info("::: CURRENT DIFFERENT TIME: {0}".format(t - self.current_time))

                if t - self.current_time > 300:
                    com = self.get_status_tcu(self.token)
                else:
                    data = self.input_commands.commands[current_command_index]
                    com = self.command_builder(data["commandId"], self.token, data)
                    current_command_index += 1
                if com.command_id == enums.COMMAND_ID.SetTcuState and com.m_state == enums.SystemState.RestMode:
                    self.waiting_self_test = True
                    self.sm.waiting_self_test = True
                if com.command_id == enums.COMMAND_ID.RunTest:
                    self.sm.waiting_run_test = True
                    self.run_count += 1
                if com.command_id == enums.COMMAND_ID.StopTest:
                    self.sm.waiting_stop_test = True
                if com.command_id == enums.COMMAND_ID.SetTcuState and com.m_state == enums.SystemState.TestInit:
                    self.sm.waiting_init_test = True


                if not self.ser.is_open:
                    self.ser.open()
                self.ser.reset_input_buffer()
                self.ser.reset_output_buffer()
                # time.sleep(0.5)
                send_length = self.ser.write(com.command_array)
                # self.ser.flush()
                time.sleep(0.08)

                # TODO read all bytes as one packet
                header = self.ser.read(4)
                command_length = com.header_length_from_bytes(header)
                while self.ser.in_waiting:
                    data = self.ser.read(command_length)
                    # self.ser.reset_input_buffer()
                    # self.ser.reset_output_buffer()
                    com.receive_response(header, data)
                    com.response.response_message()

                    self.token = self.sm.do_process(self.token, com, current_command_index, self.run_count)
                    self.current_state = self.sm.get_state()
                    logger.info("::: CURRENT APP STATE: {0}\n".format(self.current_state))
                    if self.token == -1:
                        return

                self.current_time = t
        #
        finally:
            self.finalize()


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
    start_time = app.getmseconds()
    app.exec_test()
    end_time = app.getmseconds()
    total = (end_time - start_time) / 1000
    logger.info("Complete. Total running time {:.3f} seconds".format(total))
