from commands import m_command
from input_commands import *
import switch_command
from commands import m_message
from connector import connector
import time
from commands import m_getVersion_command, m_set_TCU_state


class app:
    def __init__(self):
        self.token = 0

    def run(self):
        # creator()
        commands = input_commands()
        commands.load_commands("commands.json")
        con = connector("preferences.json")
        ser = con.get_com_port()

        while 1:
            self.token += 1
            com = m_set_TCU_state.set_TCU_state_command()
            com.command_token = self.token
            com.to_bytes()

            if not ser.is_open:
                ser.open()
            time.sleep(1)
            send_length = ser.write(com.command_array)
            ser.flush()
            if send_length > 0:
                com.send_message()

            header = ser.read(4)
            print(f'R={header} ')
            command_length = com.header_length_from_bytes(header)
            # ser.read_until(size=10)
            while ser.in_waiting:
                data = ser.readline()
                com.receive_response(header, data)
                com.response.response_message()
                print(f'Data:{data}')

            ser.close()
            if not ser.is_open:
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
