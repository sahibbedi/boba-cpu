import torch
import sys

# 1. Force PyTorch to map CUDA calls to MPS (Apple Metal)
if torch.backends.mps.is_available():
    torch.device_orig = torch.device
    def device_override(arg, *args, **kwargs):
        if isinstance(arg, str) and "cuda" in arg:
            return torch.device_orig("mps")
        return torch.device_orig(arg, *args, **kwargs)
    torch.device = device_override

    # Patch torch.cuda availability to fool scripts checking GPU status
    torch.cuda.is_available = lambda: True
    torch.cuda.current_device = lambda: 0
    torch.cuda.device_count = lambda: 1
    torch.cuda.get_device_name = lambda i=0: "AMD Radeon Pro 580X (via Metal MPS)"

    print("[Mac Patch] Metal MPS GPU emulation layer initialized.")
else:
    print("[Mac Patch] WARNING: MPS not available. Falling back to CPU.")
