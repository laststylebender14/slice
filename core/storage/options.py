from enum import Enum, auto

class Options(Enum):
    XX = auto()
    NX = auto()
    PX = auto()
    EX = auto()
    
    @classmethod
    def build(cls, option: str) -> 'Options':
        if option.upper() == Options.XX.value:
            return cls.build(xx = True)
        elif option.upper() == Options.NX.value:
            return cls.build(nx=True)
        elif option.upper() == Options.EX.value:
            return cls.build(ex=True)            
        elif option.upper() == Options.PX.value:
            return cls.build(px=True)
        return None
    
    @classmethod
    def build(cls, xx: bool = None, nx: bool = None, px: bool = None, ex:bool = None ) -> 'Options':
        if px and ex:
            raise ValueError("Only one of 'px' and 'ex' can be True")
        if xx and nx:
            raise ValueError("Only one of 'xx' and 'nx' can be True")
        if px:
            return cls.PX
        if ex:
            return cls.EX
        if xx:
            return cls.XX
        elif nx:
            return cls.NX
        else:
            return None