import os
from typing import Dict
from dotenv import load_dotenv
import pathlib

load_dotenv()

SERVER_ENV: Dict[str, str] = os.environ

class Path:

    def __init__(
        self,
        env: Dict[str, str] = SERVER_ENV
    ) -> None:
        
        self.env: Dict[str, str] = env
        self.base_path: pathlib.Path = pathlib.Path(
            self.env['INTERNAL_LOG_LOCATION']
        )
        self.log: pathlib.Path = self.base_path / SERVER_ENV['LOG_FILE_NAME']

PATH: Path = Path()