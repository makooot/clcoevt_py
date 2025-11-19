class Message:
    class Severities:
        DEBUG = 7
        INFO = 6
        NOTE = 5
        WARN = 4
        ERROR = 3
        CRIT = 2
        ALERT = 1
        EMERG = 0

    severity_string = [
        "Emergency",
        "Alert",
        "Critical",
        "Error",
        "Warning",
        "Notice",
        "Infomational",
        "Debug",
    ]

    def __init__(
        self,
        msgid="-",
        severities=4,
        text=None,
    ):
        self.msgid = msgid
        if severities < 0 or severities > 7:
            self.severities = 4
        else:
            self.severities = severities
        self.text = text

    def __str__(self):
        return (
            self.msgid + ": " + self.severity_string[self.severities] + ": " + self.text
        )


class MessageNotFound(Message):
    def __init__(self, var_name):
        super().__init__("NOT_FOUND", Message.Severities.NOTE, "Not found: " + var_name)


class MessageInvalidValue(Message):
    def __init__(self, var_name, value):
        super().__init__(
            "INVALID_VALUE",
            Message.Severities.WARN,
            "Invalid value: " + var_name + "=" + value,
        )


class MessageInvalidValueS(Message):
    def __init__(self, s):
        super().__init__(
            "INVALID_VALUE",
            Message.Severities.WARN,
            "Invalid value: " + str(s),
        )


class MessageInvalidType(Message):
    def __init__(self, s):
        super().__init__(
            "INVALID_TYPE",
            Message.Severities.WARN,
            "Invalid type: " + str(s),
        )


class MessageInvalidSetting(Message):
    def __init__(self, setting):
        super().__init__(
            "INVALID_SETTING",
            Message.Severities.ERROR,
            "Invalid setting: " + str(setting),
        )


class MessageFileNotFound(Message):
    def __init__(self, filename):
        super().__init__(
            "FILE_NOT_FOUND",
            Message.Severities.NOTE,
            "File not found: " + str(filename),
        )


class MessageInvalidTomlValue(Message):
    def __init__(self, name, value):
        if isinstance(value, bool):
            value_str = "true" if value else "false"
        elif isinstance(value, str):
            value_str = '"' + value + '"'
        elif type(value) is int:
            value_str = str(value)
        else:
            value_str = str(value)
        super().__init__(
            "INVALID_TOML_VALUE",
            Message.Severities.WARN,
            "Invalid value: " + str(name) + "=" + value_str,
        )


class MessageInvalidTomlFile(Message):
    def __init__(self, filename):
        super().__init__(
            "INVALID_TOML_FILE",
            Message.Severities.WARN,
            "Invalid TOML file: " + str(filename),
        )
