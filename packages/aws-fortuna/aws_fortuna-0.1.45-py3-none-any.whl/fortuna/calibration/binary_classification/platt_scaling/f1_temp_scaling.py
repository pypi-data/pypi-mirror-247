import numpy as np
from scipy.optimize import brute

from fortuna.calibration.binary_classification.platt_scaling.base import (
    BaseBinaryClassificationPlattScaling,
)


class F1BinaryClassificationPlattScaling(
    BaseBinaryClassificationPlattScaling
):
    """
    A Platt scaling class for binary classification.
    It learns a linear transformation of the probability that the target variable is positive.
    The method attempts to maximize the F1 score.
    """

    def __init__(self):
        super().__init__()
        self._threshold = None

    def fit(self, probs: np.ndarray, targets: np.ndarray, threshold: float):
        self._check_probs(probs)
        self._check_targets(targets)

        self._threshold = threshold
        n_pos_targets = np.sum(targets)

        def loss_fn(params):
            temp_preds = np.clip(params[0] + params[1] * probs, 0, 1) >= threshold
            n_pos_preds = np.sum(temp_preds)
            n_joint = np.sum(targets * temp_preds)
            prec = n_joint / n_pos_preds if n_pos_preds > 0 else 0.0
            rec = n_joint / n_pos_targets
            if prec + rec == 0.0:
                return 0.0
            return -2 * prec * rec / (prec + rec)

        self._intercept, self._slope = brute(
            loss_fn, ranges=[(-1, 1), (np.min(probs), 1 / threshold)], Ns=100
        )

    def predict(self, probs: np.ndarray):
        self._check_probs(probs)
        return (self.predict_proba(probs) >= self._threshold).astype(int)

    @property
    def threshold(self):
        return self._threshold
