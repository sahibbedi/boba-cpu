# Mock pycuda.driver for macOS OpenGL / MPS execution

class _MemoryType:
    HOST = 1
    DEVICE = 2
    ARRAY = 3
    UNIFIED = 4

memory_type = _MemoryType()

class Memcpy2D:
    def __init__(self):
        self.src_pitch = 0
        self.dst_pitch = 0
        self.width_in_bytes = 0
        self.height = 0
        self.src_device = None
        self.dst_device = None
        self.src_memory_type = 0
        self.dst_memory_type = 0

    def __call__(self, stream=None, aligned=False):
        pass

    def execute(self, stream=None):
        pass

class Stream:
    def synchronize(self):
        pass

class Context:
    @classmethod
    def attach(cls):
        return cls()

    @classmethod
    def get_current(cls):
        return cls()

    def push(self):
        pass

    def pop(self):
        pass

    def synchronize(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class Device:
    def __init__(self, idx=0):
        self.idx = idx

    def make_context(self):
        return Context()

    def retain_primary_context(self):
        return Context()

def init():
    pass

def PagelockedArg(*args, **kwargs):
    pass
