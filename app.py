from commands import m_command
from input_commands import *
import switch_command
from commands import m_message
from connector import connector
import time
import serial


def run():

    SetTcuState = [0xc0, 0x0, 0xa, 0x29, 0x0, 0x0, 0x0, 0x1, 0x0, 0x0, 10, 13]

    # creator()
    # commands = input_commands()
    # commands.load_commands("commands.json")
    #
    # com = m_command.command()
    # com.command_token = 2
    # com.command_id = m_message.COMMAND_ID["GetVersion"]
    # com.to_bytes()
    #
    #
    # con = connector("preferences.json")
    # ser = con.get_com_port()

    # ser = con.create_com_port()
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = 'COM3'
    ser.timeout = 0.5
    ser.write_timeout = 0.5
    ser.open()


    while 1:
        if not ser.is_open:
            ser.open()
        time.sleep(1)

        l = [118, 0, 8, 37, 0, 0, 0, 2, 0]
        l1 = [192, 0, 10, 41, 0, 0, 0, 1, 0, 10, 13]
        len = ser.write(l1)

        ser.flush()

        r = ser.read(4)
        print(f'R={r} ')
        # ser.read_until(size=10)
        while ser.in_waiting:
            data = ser.readline().decode("ascii")
            print(f'Data={data} length: {len(data)}')

        ser.close()
        if not ser.is_open:
            print('port close')


def creator():
    switch = switch_command()
    switch.get_command('GetCommandTCU')


if __name__ == '__main__':
    import logging.config
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
    logging.info('start app module.')
    run()