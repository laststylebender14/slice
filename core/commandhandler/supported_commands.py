from enum import Enum

class SupportedCommands(Enum):
    SET = "set"
    GET = "get"
    
    SETNX = "setnx"
    SETXX = "setxx"
    
    GETDEL = "getdel"
    PING = "ping"
    ECHO = "echo"
    