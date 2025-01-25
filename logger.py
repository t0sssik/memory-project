import yaml
import struct
import shutil
from pathlib import Path
import matplotlib.pyplot as plt


class Logger():
    def __init__(self, hparams_path:str):
        if not Path.exists(Path("loggs")):
            Path.mkdir("loggs")
            with open(Path("loggs/version_number.bin"), "wb") as file:
                binary_data = struct.pack("i", 0)
                file.write(binary_data)
            
        with open(Path("loggs/version_number.bin"), "rb") as file:
            binary_data = file.read()
            version_number = struct.unpack('i', binary_data)[0]
        
        self.log_path = Path("loggs") / Path(f"version_{version_number}")
        Path.mkdir(self.log_path)
        
        with open(Path("loggs/version_number.bin"), "wb") as file:
            binary_data = struct.pack("i", version_number + 1)
            file.write(binary_data)
        
        self.hparams_path = Path(hparams_path)
        shutil.copy(self.hparams_path, self.path)
        
        
if __name__ == "__main__":
    logger = Logger("hparams.yaml")