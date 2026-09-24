# Mock pycuda.gl for macOS OpenGL rendering pipeline

class _GraphicsMapFlags:
    NONE = 0
    READ_ONLY = 1
    WRITE_DISCARD = 2

graphics_map_flags = _GraphicsMapFlags()

class RegisteredBuffer:
    def __init__(self, buffer_id=None, flags=0):
        self.buffer_id = buffer_id
        self.flags = flags

    def map(self):
        return self

    def unmap(self):
        pass

    def unregister(self):
        pass

    def device_ptr_and_size(self):
        return (0, 0)
