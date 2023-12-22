import numpy as np
import pandas as pd
from sklearn.preprocessing import Normalizer, StandardScaler


def normalize(data: pd.Series) -> pd.Series:
    """
        L1 Normalization.

        Parameters:
            data (Series): Input Data
        Returns:
            data (Series):  Transformed Data
    """
    return Normalizer(norm="l1").fit_transform(data.values.reshape(1, -1)).T


def standard_scale(data: pd.Series) -> pd.Series:
    """
        Scale the data to zero mean and unit variance.

        Parameters:
            data (Series): Input Data
        Returns:
            data (Series):  Transformed Data
    """
    return StandardScaler().fit_transform(data.values.reshape(-1, 1))


if __name__ == "__main__":
    csv_path = "./test.csv"
    data = pd.read_csv(csv_path)
    data = data.dropna()
    print(data.describe())
    data["normalized"] = normalize(data=data['10YTY_Q_Q_percentage'])
    data["scaled"] = standard_scale(data=data['10YTY_Q_Q_percentage'])
    print(data.describe())