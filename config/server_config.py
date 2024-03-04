from core.logger import logger

class ServerConfig:
    _instance = None
    _host = "localhost"
    _port = 6379
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @property
    def host(self) -> str:
        return self._host
    
    @property
    def port(self) -> int:
        return self._port

    @host.setter
    def host(self, host: str = "localhost") -> None:
        self._host = host

    @port.setter
    def port(self, port: int = 6379) -> None:
        try:
            self._port = int(port, base=10)
        except ValueError as err:
            logger.error(
                f"PORT env can't be parsed, reverting to default port : {self._port} "
            )

    def __str__(self) -> str:
        return f"host:{self._host} port:{self._port}"
