```python
import numpy as np

def top_k_above_threshold(scores: np.ndarray, k: int, threshold: float) -> np.ndarray:
    """
    Returns the indices of the top-k scores in a (1, n) array where scores > threshold.
    
    Args:
        scores (np.ndarray): A 1 x n NumPy array of scores.
        k (int): Number of top scores to select.
        threshold (float): Minimum threshold value to consider.
    
    Returns:
        np.ndarray: Indices of the top-k scores above the threshold.
    """
    # Flatten to 1D in case it's a (1, n) shape
    scores_flat = scores.flatten()

    # Get indices where scores > threshold
    valid_indices = np.where(scores_flat > threshold)[0]

    if len(valid_indices) == 0:
        return np.array([], dtype=int)  # No scores above threshold

    # Filter the valid scores
    filtered_scores = scores_flat[valid_indices]

    # Get indices of the top-k scores
    topk_relative_indices = np.argsort(filtered_scores)[-k:][::-1]
    topk_indices = valid_indices[topk_relative_indices]

    return topk_indices

# Example usage
scores = np.array([[0.1, 0.7, 0.4, 0.95, 0.2, 0.85]])
k = 3
threshold = 0.5
result = top_k_above_threshold(scores, k, threshold)
print("Top-k indices where score > threshold:", result)
```
