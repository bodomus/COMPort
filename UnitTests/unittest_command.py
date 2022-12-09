import unittest
from Utilities import converters
from commands import m_getVersion_command, m_message, m_set_TCU_state


class get_version_TestCase(unittest.TestCase):
    def setUp(self):
        self.get_version_buffer = [73, 0, 8, 37, 0, 0, 0, 1, 0]
        self.token = 1
        self.set_TCU_command_buffer = [0xc0, 0x0, 0xa, 0x29, 0x0, 0x0, 0x0, 0x1, 0x0, 0x0, 0x0]

    def test_check_create_get_version_command_return_valid_command(self):
        com = m_getVersion_command.getVersion_command()

        com.command_token = self.token
        com.command_id = m_message.COMMAND_ID["GetVersion"]
        com.to_bytes()
        self.assertEqual(self.get_version_buffer, com.command_array)

    def test_check_create_set_TCU_state_command_return_valid_command(self):
        com = m_set_TCU_state.set_TCU_state_command()

        com.command_token = self.token
        com.command_id = m_message.COMMAND_ID["SetTcuState"]
        com.to_bytes()
        self.assertEqual(self.set_TCU_command_buffer, com.command_array)
