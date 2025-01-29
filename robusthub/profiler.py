import torch

import time

class Profiler:
    """
    Memory and runtime profiler used in benchmarks.

    Parameters
    -----------
    device
        PyTorch device to monitor.
    """
    def __init__(self, device: torch.device):
        self.device = device

        self.start_time_ = 0
        self.end_time_ = 0
        self.memory = 0

    def __enter__(self):
        self.start_time_ = time.time()
        torch.cuda.reset_peak_memory_stats(self.device)
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time_ = time.time()
        self.memory = torch.cuda.max_memory_allocated(self.device)
    
    @property
    def runtime(self):
        return self.end_time_ - self.start_time_
