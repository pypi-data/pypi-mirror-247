from nvitop import Device
import torch
import threading 
from time import sleep
import argparse

class Consumer:
    def __init__(self, device_index, memory_free_percent) -> None:
        self.stop_flag = False
        self.device_index = device_index
        self.memory_free_percent = memory_free_percent
        self.thread_task = threading.Thread(target=self.consume, args=(lambda: self.stop_threads, self.device_index), daemon=True) 
        
        self.devices = []
        for i in device_index:
            self.devices.append(Device(index=i))

        print(f"{'Fan speed':^15}|{'Temperature':^15}|{'GPU utilization':^20}|{'Memory Free/Memory Total':^40}")

    def start(self):
        self.thread_task.start()

    def join(self):
        self.thread_task.join()
    
    def stop(self):
        self.stop_flag = True

    def resume(self):
        self.stop_flag = False

    def consume(self, stop_flag, device_index):
        memory_frees = self.showGPU()
        datas = []
        for i, device in enumerate(device_index):
            data_size = (memory_frees[i] * self.memory_free_percent / 100) // (32 / 8)
            data_size = int(data_size)
            data = torch.rand(data_size, dtype=torch.float32, device=device)
            datas.append(data)
        while not self.stop_flag:
            for data in datas:
                data.add_(1).sub_(1)
            self.showGPU()
        
        print('\n\n')

    def showGPU(self):
        memory_frees = []
        info = {
            'fan_speed': '',
            'temperature': '',
            'gpu_utilization': '',
            'memory': '',
        }
        for device in self.devices:
            info['fan_speed'] += f'{device.fan_speed()}% '
            info['temperature'] += f'{device.temperature()}C '
            info['gpu_utilization'] += f'{device.gpu_utilization()}% '
            info['memory'] += f'{device.memory_used_human()}/{device.memory_total_human()} '
            memory_frees.append(device.memory_free())

        result = f"{info['fan_speed']:^15}|{info['temperature']:^15}|{info['gpu_utilization']:^20}|{info['memory']:^40}"
        print(result, end='\r')

        return memory_frees

class WatchDog:
    def __init__(self) -> None:
        self.stop_flag = False
        self.thread_task = threading.Thread(target=self.watch)
        self.thread_task.start()

    def watch(self):
        while input() != 'q':
            sleep(0.5)

def main():
    assert torch.cuda.is_available(), 'check your cuda'
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--device_index', nargs='+', type=int)
    parser.add_argument('--memory_free_percent', default=10, type=int)
    args = parser.parse_args()

    if args.device_index is None:
        count = torch.cuda.device_count()
        device_index = [i for i in range(count)]
    else:
        device_index = args.device_index
    print('device_index', device_index)
    
    consumer = Consumer(device_index, args.memory_free_percent)
    consumer.start()

    watchDog = WatchDog()

if __name__ == '__main__':
    main()