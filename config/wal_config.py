class WalConfig:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def set_wal_enable(self, status : bool = False) -> None:
        self.enable = status

    def set_path(self, path : str = "./") -> None:
        self.path = path

    def is_wal_enabled(self):
        return self.enable

    def get_path(self):
        return self.path
    
    def __str__(self) -> str:
        return f"{self.enable} {self.path}"
    
    