COMMAND_ID = {
    'Undefined': -1,
    'ProtocolError': 0,
    'RunTest':  22,
    'EndTest': 25,
    'ClearCommandBuffer': 27,
    'FiniteRampByTime': 28,
    'FiniteRampByTemperature': 29,
    'InfiniteRamp': 30,
    'GetStatusTCU': 33,
    'GetVersion': 37,
    'SetTcuState': 41,
    'SimulateResponseUnit': 45,
    'StopTest': 47,
    'GetCurrentPID': 70,
    'FiniteRampByRate': 85,
}

System_State = {
    'SafeMode': 0,
    'SelfTest': 1,
    'RestMode': 2,
    'TestInit': 3,
    'TestRun': 4,
    'TestPaused': 5,
    'Engineering': 6,
    'FrimwareUpdate': 7,
    'WritingBlackBox': 8
}

ID_TO_COMMAND = {item: key for key, item in COMMAND_ID.items()}


MAX_LENGTH = 512


class message():
    def __init__(self):
        self.command_id = COMMAND_ID['Undefined']
        self.command_array = None
        self.command_token = None
        self.command_tag = None

    def __str__(self):
        return f"command_id: {self.command_id} command_token: {self.command_token} command_tag: {self.command_tag}"
