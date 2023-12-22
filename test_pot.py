import numpy as np

def adjust_predicts(score, label,
                    threshold=None,
                    pred=None,
                    calc_latency=False):
    """
    Calculate adjusted predict labels using given `score`, `threshold` (or given `pred`) and `label`.
    Args:
        score (np.ndarray): The anomaly score
        label (np.ndarray): The ground-truth label
        threshold (float): The threshold of anomaly score.
            A point is labeled as "anomaly" if its score is lower than the threshold.
        pred (np.ndarray or None): if not None, adjust `pred` and ignore `score` and `threshold`,
        calc_latency (bool):
    Returns:
        np.ndarray: predict labels
    """
    if len(score) != len(label):
        raise ValueError("score and label must have the same length")
    score = np.asarray(score)
    label = np.asarray(label)
    latency = 0
    if pred is None:
        predict = score > threshold
    else:
        predict = pred
    actual = label > 0.1
    anomaly_state = False
    anomaly_count = 0
    for i in range(len(score)):
        if actual[i] and predict[i] and not anomaly_state:
                anomaly_state = True
                anomaly_count += 1
                for j in range(i, 0, -1):
                    if not actual[j]:
                        break
                    else:
                        if not predict[j]:
                            predict[j] = True
                            latency += 1
        elif not actual[i]:
            anomaly_state = False
        if anomaly_state:
            predict[i] = True
    if calc_latency:
        return predict, latency / (anomaly_count + 1e-4)
    else:
        return predict
    
    
if __name__ == "__main__":
    # Found one anomalous observation at the start of the actual anomaly
    score = np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 0])
    label = np.array([0, 0, 1, 1, 1, 1, 1, 0, 0, 0])
    adjust_predicts(score, label, threshold=0)
    
    # Found one anomalous observation at the end of the actual anomaly
    score = np.array([0, 0, 0, 0, 0, 0, 1, 0, 0, 0])
    label = np.array([0, 0, 1, 1, 1, 1, 1, 0, 0, 0])
    adjust_predicts(score, label, threshold=0)
    
    # Found one anomalous observation in the middle of the actual anomaly
    score = np.array([0, 0, 0, 0, 1, 0, 0, 0, 0, 0])
    label = np.array([0, 0, 1, 1, 1, 1, 1, 0, 0, 0])
    adjust_predicts(score, label, threshold=0)
    
    # Found anomalous observations where there are no actual anomalies
    score = np.array([0, 0, 1, 1, 1, 0, 0, 0, 0, 0])
    label = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    adjust_predicts(score, label, threshold=0)
    
    # Found too many anomalous observations
    score = np.array([0, 0, 1, 1, 1, 0, 0, 0, 0, 0])
    label = np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 0])
    adjust_predicts(score, label, threshold=0)
    
    # Found only one anomaly
    score = np.array([0, 0, 1, 1, 0, 0, 0, 0, 0, 0])
    label = np.array([0, 0, 1, 1, 0, 1, 1, 0, 0, 0])
    adjust_predicts(score, label, threshold=0)