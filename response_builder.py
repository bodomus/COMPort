from commands.r_finite_ramp_by_time import finite_ramp_by_time_response
from commands.r_get_status_TCU import get_statusTCU_response
from commands.r_get_version_command import get_version_response
from commands.response import response


def build_response(command_id):
    """ """
    if command_id == 19:  # get GetActiveThermode
        self.response = response()
    if command_id == 33:  # get status TCU
        self.response = get_statusTCU_response()
    if command_id == 22:  # RunTest
        self.response = response()
    if command_id == 27:  # ClearCommandBuffer
        self.response = response()
    if command_id == 37:
        self.response = get_version_response()
    if command_id == 41:  # SetTcuState
        self.response = response()
    if command_id == 47:  # StopTest
        self.response = response()
    if command_id == 25:  # EndTest
        self.response = response()
    if command_id == 45:  # SimulateResponseUnit
        self.response = response()
    if command_id == 28:  # FiniteRampBytime
        self.response = finite_ramp_by_time_response()