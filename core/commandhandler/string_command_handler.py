from typing import List
from enum import Enum

from core.storage.kv_store import Store
from core.interactors.string_interactor import StringInteractor
from core.resp.encoder import encode_simple_strings_resp, encode_bulk_strings_reps,encode_null_string_resp
from core.storage.node import Node
from core.types.structure_types import StructureType
from core.storage.options import Options
from core.aof.aof import WAL
from core.aof.aof_entry import AOFEntry
from core.commandhandler.supported_commands import SupportedCommands

class StringOptions(Enum):
    NX = "nx"
    XX = "xx"
    EX = "ex"
    PX = "px"

class StringCommandHandler:
    def __init__(self, store:Store, walFile:WAL = None) -> None:
        self.interactor = StringInteractor(store=store)
        self.walFile = walFile
        
    def log(self,operation: SupportedCommands, aofEntry: AOFEntry) -> None:
        print("[Logging]:", operation.value, aofEntry)
        self.walFile.log(operation,aofEntry)
        
    def setnx(self, commands: List[str]) -> str:
        commandSize = len(commands)
        if commandSize < 2:
            return encode_bulk_strings_reps("ERR Syntax error")
        
        key, value = commands
        
        resp = self.interactor.setnx(key=key,value=Node(value=value,type=StructureType.STRING),options=Options("nx"))    # {0 - exits,-1 -> not,1 -> inserted} 
        if resp == 1:
            self.log(SupportedCommands.SET,AOFEntry(key=key,value=value,options=Options("nx")))
            return encode_simple_strings_resp("OK")
        return encode_null_string_resp()

    
    def setxx(self, commands: List[str]) -> str:
        commandSize = len(commands)
        if commandSize < 2:
            return encode_bulk_strings_reps("ERR Syntax error")
        
        key, value = commands
            
        resp = self.interactor.setxx(key=key,value=Node(value=value,type=StructureType.STRING),options=Options("xx"))    # {0 - exits,-1 -> not,1 -> inserted} 
        if resp == 1:
            self.log(SupportedCommands.SET,AOFEntry(key=key,value=value,options=Options("xx")))
            return encode_simple_strings_resp("OK")
        return encode_null_string_resp()
    
    def set(self, commands: List[str]) -> str:
        """
            commands are in the form of.
            len(commands) ==  2 then  ["KEY","VALUE"]
            len(commands) ==  3 then  ["KEY","VALUE","NX/XX"]
            len(commands) ==  4 then  ["KEY","VALUE","EX/PX","EXP_TIME"]
            len(commands) ==  5 then  ["KEY","VALUE","NX/PX","EX/PX","EXP_TIME"]
        """
        commandSize = len(commands)
        if commandSize not in [2,3,4,5] or commandSize < 2:
            return encode_bulk_strings_reps("ERR Syntax error")
        
        if commandSize == 2:     
            key, value = commands
            resp = self.interactor.set(key=key,value=Node(value=value,type=StructureType.STRING))
            if resp == 1 or resp == 0:
                self.log(SupportedCommands.SET,AOFEntry(key=key,value=value))
                return encode_simple_strings_resp("OK")
            return encode_null_string_resp()
        
        elif commandSize == 3:
            key, value, option = commands
            processedOption = option.strip().lower()
            
            if processedOption == StringOptions.XX.value:
                return self.setxx(commands[:-1])
            elif processedOption == StringOptions.NX.value:
                return self.setnx(commands[:-1])
            return encode_bulk_strings_reps("ERR Syntax error")
            
        elif commandSize == 4:
            key, value, exp_command, exp_time = commands
            expiration = exp_time
            processed_command = exp_command.strip().lower()
            
            if processed_command not in ["ex","px"]:
                return encode_bulk_strings_reps("ERR Syntax error")
                
            if processed_command == StringOptions.PX.value:
                options = Options("px")
            elif processed_command == StringOptions.EX.value:
                options = Options("ex")
            
            resp = self.interactor.set(key=key,value=Node(value=value,type=StructureType.STRING, ttl=expiration), options= options)
            if resp == 1:
                self.log(SupportedCommands.SET,AOFEntry(key=key,value=value,ttl=expiration,options=options))
                return encode_simple_strings_resp("OK")
            return encode_null_string_resp()
            
        return encode_null_string_resp()
            
    def get(self, commands: List[str]) -> str:
        key = commands[0]
        resp:(Node | None) = self.interactor.get(key=key)
        if resp is None:
            return encode_null_string_resp()
        return encode_bulk_strings_reps(resp=resp.value)
    
    def delete(self, commands: List[str]) -> str:
        key = commands[0]
        resp: (Node | None) = self.interactor.delete(key=key)
        if resp:
            self.log(SupportedCommands.GETDEL,AOFEntry(key=key))
            return encode_bulk_strings_reps(resp=resp.value)
        return encode_null_string_resp()
        