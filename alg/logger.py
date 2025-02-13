import struct
import shutil
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


class Logger():
    def __init__(self, hparams_path: str):
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
        shutil.copy(self.hparams_path, self.log_path)

        self.data = pd.DataFrame(columns=[
            'iter_number',
            'best_ff',
            'avg_difficulty',
            'memory_count',
            'attention_count',
            'recognition_count',
            'action_count',
            'speech_count',
        ])


    def add_data(self,
                 iter_number:int,
                 best_ff:float,
                 avg_difficulty:float,
                 tasks_counter:dict
                 ) -> None:
        self.data.loc[iter_number] = [
            iter_number,
            best_ff,
            avg_difficulty,
            tasks_counter['MEMORY'],
            tasks_counter['ATTENTION'],
            tasks_counter['RECOGNITION'],
            tasks_counter['ACTION'],
            tasks_counter['SPEECH'],
        ]
    
    
    def save_data(self):
        self.data.to_csv(self.log_path / Path("data.csv"))
        
        
    def show_progress_plot(self):
        x = self.data["iter_number"]
        plt.plot(x, self.data["best_ff"], label="Лучшая фф")
        plt.title("График изменения лучшей фитнес-функции")
        plt.legend()
        plt.xlabel("Номер итерации")
        plt.ylabel("Значение фитнес-функции")
        plt.grid(True)
        plt.savefig(self.log_path / Path("progress_plot.png"))
        plt.close()
        
        
    def show_avg_difficulty_plot(self):
        x = self.data["iter_number"]
        plt.plot(x, self.data["avg_difficulty"], label="Средняя сложность")
        plt.title("График изменения средней сложности")
        plt.legend()
        plt.xlabel("Номер итерации")
        plt.ylabel("Средняя сложность набора")
        plt.grid(True)
        plt.savefig(self.log_path / Path("avg_difficulty_plot.png"))
        plt.close()
        
    
    def show_tasks_counter_plot(self):
        x = self.data["iter_number"]
        plt.plot(x, self.data["memory_count"], label="Заданий на память")
        plt.plot(x, self.data["attention_count"], label="Заданий на внимание")
        plt.plot(x, self.data["recognition_count"], label="Заданий на распознавание")
        plt.plot(x, self.data["action_count"], label="Заданий на действие")
        plt.plot(x, self.data["speech_count"], label="Заданий на речь")
        plt.title("График изменения кол-ва заданий каждого типа")
        plt.legend()
        plt.xlabel("Номер итерации")
        plt.ylabel("Число заданий")
        plt.grid(True)
        plt.savefig(self.log_path / Path("tasks_counter_plot.png"))
        plt.close()