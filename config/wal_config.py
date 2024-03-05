from core.logger import logger

class WalConfig:
    _instance = None
    _wal_enable: bool = False
    _path: str = "./aof.slice"
    _flush_frequency: int = (
        1000  # after 1000 keys change, it will flush buffer aof data to disk.
    )
    _ttl_normalizer: int = (
        1709618598664  # why this default time? this is when slice-db was born officially ;).
    )

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

    @property
    def ttl_normalizer(self) -> int:
        return self._ttl_normalizer

    @ttl_normalizer.setter
    def ttl_normalizer(self, ttl_normalizer) -> int:
        try:
            self._ttl_normalizer = int(ttl_normalizer, base=10)
        except ValueError:
            logger.warn(
                f"failed to parse ttl_normalizer, reverting to default : {self._ttl_normalizer}"
            )

    @flush_frequency.setter
    def flush_frequency(self, flush_frequency: int):
        try:
            self._flush_frequency = int(flush_frequency, base=10)
        except ValueError:
            logger.warn(
                f"failed to parse flush frequency, reverting to default : {self._flush_frequency}"
            )

    @wal_enable.setter
    def wal_enable(self, status: bool = False) -> None:
        self._wal_enable = status == "True"

    @path.setter
    def path(self, path: str = "./") -> None:
        self._path = path

    def __str__(self) -> str:
        return f"isEnabled:{self._wal_enable} path:{self._path} flush_frequency:{self._flush_frequency} ttl_normalizer:{self._ttl_normalizer}"