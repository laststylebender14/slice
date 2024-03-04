from core.logger import logger

class WalConfig:
    _instance = None
    _wal_enable: bool = False
    _path: str = "./aof.slice"
    _flush_frequency: int = 1000 # after 1000 keys change, it will flush buffer aof data to disk.
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @property
    def wal_enable(self) -> bool:
        return self._wal_enable
    
    @property
    def path(self) -> str:
        return self._path
    
    @property
    def flush_frequency(self) -> int:
        return self._flush_frequency
    
    @flush_frequency.setter
    def flush_frequency(self, flush_frequency: int):
        try:
            self._flush_frequency = int(flush_frequency)
        except ValueError:
            logger.warn(f"failed to prase flush frequency, reverting to default : {self._flush_frequency}")
    
    @wal_enable.setter
    def wal_enable(self, status : bool = False) -> None:
        self._wal_enable = status == "True"

    @path.setter
    def path(self, path : str = "./") -> None:
        self._path = path

    def __str__(self) -> str:
        return f"isEnabled:{self._wal_enable} path:{self._path} flush_frequency:{self._flush_frequency}"
    
    