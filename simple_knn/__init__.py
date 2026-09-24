import torch
import numpy as np
from scipy.spatial import KDTree

class _C_Shim:
    @staticmethod
    def distCUDA2(points):
        # points: [N, 3] torch.Tensor
        is_tensor = isinstance(points, torch.Tensor)
        device = points.device if is_tensor else "cpu"
        
        pts_np = points.detach().cpu().numpy() if is_tensor else np.asarray(points)
        
        # Build KDTree for k=4 (point itself + 3 nearest neighbors)
        tree = KDTree(pts_np)
        k = min(4, len(pts_np))
        dists, _ = tree.query(pts_np, k=k)
        
        # Exclude self-distance (column 0) and average the square of the 3 neighbors
        if dists.shape[1] > 1:
            mean_sq_dist = np.mean(dists[:, 1:] ** 2, axis=1)
        else:
            mean_sq_dist = np.zeros(len(pts_np), dtype=np.float32)
            
        res = torch.from_numpy(mean_sq_dist.astype(np.float32))
        return res.to(device) if is_tensor else res

_C = _C_Shim()
