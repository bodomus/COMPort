ThermodeType = {
    'CHEPS': 0,
    'TSA': 1,
    'Algometer': 2,
    'Vibratory': 3,
    'AirTSA': 4,
    'CoolingUnit': 5,
    'TSASlave': 6,
    'DCHEPS': 7,
    'Undefined': 255
}

TsaModel = {
    'Large30x30': 0,
    'Small16x16': 1,
    'Small5x5': 2,
    'Small2x2': 3,
    'IntraOral': 4,
    'GSA': 5,
    'Fmri_Large30x30': 6,
    'Fmri_Small16x16': 7,
    'Fmri_Small5x5': 8,
    'Fmri_Small2x2': 9,
    'Fmri_IntraOral': 10,
    'Fmri_GSA': 11,
    'CPM_Hot': 12,
    'CPM_Cold': 13,
    'Unknown': 255
}

HealthStatus = {
        'Ok':  0,
        'APosVoltageFailure': 1,                 # APOS voltage is out of range
        'VPVoltageFailure': 2,                   # VP voltage is out of range
        'VrefVoltageFailure': 4,                 # Vref voltage is out of range
        'MTECCurrentFailure': 8,                 # Main TEC driver current is out of range
        'RTECCurrentFailure': 16,                # Reference TEC driver current is out of range
        'MTECVoltageFailure': 32,                # Main TEC driver voltage is out of range
        'RTECVoltageFailure': 64,                # Reference TEC driver voltage is out of range
        'PumpCurrentFailure': 128,               # Pump current is out of range
        'WDTSelfTestFailureOffset': 256,         # WDT self-test failed
        'EmergencyButtonStatusOffset': 512,      # Emergency button pressed
        'WaterLevelWarningOffset': 1024,         # Water level is too low
        'MFanFailureOffset': 2048,               # Main thermode fan rotor locked
        'RFanFailureOffset': 4096,               # Reference thermode fan rotor locked
        'ICUFanFailureOffset': 8192,             # Cooling unit fan rotor locked
        'ICUPumpFailureOffset': 16384,           # Cooling unit pump rotor locked
        'ICUTECFailureOffset': 32768             # Cooling unit TEC doesn't respond
}


ACKCODE = {
    'Ok': 0,
    'UnsupportedCommand': 1,
    'WrongCRC': 2,
    'IllegalParameter': 3,
    'IllegalState': 4,
    'ThermodeDisabled': 5,
    'IllegalCommandSequence': 6,
    'BufferFull': 7,
    'NoDataExists': 8,
    'DataAlreadyExists': 9,
    'Fail': 10,  # Error during process command
    'WrongFlashAddress': 11,  # Error during process command
    'WrongSize': 12,  # Error during process command
    'Undefined': 255
}

ID_TO_ACKCODE = {item: key for key, item in ACKCODE.items()}

