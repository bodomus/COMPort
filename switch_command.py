from commands import m_getstatusTCU_command
from commands import m_getVersion_command
from commands import m_finite_ramp_by_time_command


class switch_command:
    def get_command(self, command):
        default = None

        return getattr(self, command, lambda: default)()

    def GetStatusTCU(self):
        return m_getstatusTCU_command.get_status_TCU_command()

    def GetVersion(self):
        return m_getVersion_command()

    def FiniteRampByTime(self):
        return m_finite_ramp_by_time_command()