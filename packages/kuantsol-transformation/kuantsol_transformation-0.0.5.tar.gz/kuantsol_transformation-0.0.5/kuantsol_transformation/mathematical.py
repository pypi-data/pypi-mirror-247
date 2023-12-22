import numpy as np
import pandas as pd


def ln(data: pd.Series) -> pd.Series:
    """
        Ln transformation

        Parameters:
            data (Series): Input Data
        Returns:
            data (Series):  Transformed Data
    """
    return np.log(data)


def exp(data: pd.Series) -> pd.Series:
    """
        Exponential transformation

        Parameters:
            data (Series): Input Data
        Returns:
            data (Series):  Transformed Data
    """
    return np.exp(data)


def square(data: pd.Series) -> pd.Series:
    """
        Square transformation

        Parameters:
            data (Series): Input Data
        Returns:
            data (Series):  Transformed Data
    """
    return np.square(data)


def square_root(data: pd.Series) -> pd.Series:
    """
        Square-Root transformation

        Parameters:
            data (Series): Input Data
        Returns:
            data (Series):  Transformed Data
    """
    return np.sqrt(data)


def inverse(data: pd.Series) -> pd.Series:
    """
        Inverse (1/X) of data.

        Parameters:
            data (Series): Input Data
        Returns:
            data (Series):  Transformed Data
    """
    return np.reciprocal(data)


def power(data: pd.Series, n: int = 3) -> pd.Series:
    """
        X^n.

        Parameters:
            data (Series): Input Data
            n (Series): Power
        Returns:
            data (Series):  Transformed Data
    """
    return np.power(data, n)


def one_over_power(data: pd.Series, n: int = 3) -> pd.Series:
    """
        1/X^n.

        Parameters:
            data (Series): Input Data
            n (Series): Power
        Returns:
            data (Series):  Transformed Data
    """
    return inverse(np.power(data, n))


def log10(data: pd.Series) -> pd.Series:
    """
        Log10 transformation.

        Parameters:
            data (Series): Input Data
        Returns:
            data (Series):  Transformed Data
    """
    return np.log10(data)


def log2(data: pd.Series) -> pd.Series:
    """
        Log2 transformation.

        Parameters:
            data (Series): Input Data
        Returns:
            data (Series):  Transformed Data
    """
    return np.log2(data)


def one_over_one_minus_x(data: pd.Series) -> pd.Series:
    """
        1/(1-X).

        Parameters:
            data (Series): Input Data
        Returns:
            data (Series):  Transformed Data
    """
    return 1 / (1 - data)


def one_over_one_plus_x(data: pd.Series) -> pd.Series:
    """
        1/(1+X).

        Parameters:
            data (Series): Input Data
        Returns:
            data (Series):  Transformed Data
    """
    return 1 / (1 + data)


def one_over_x_minus_one(data: pd.Series) -> pd.Series:
    """
        1/(X-1).

        Parameters:
            data (Series): Input Data
        Returns:
            data (Series):  Transformed Data
    """
    return 1 / (data - 1)


def threshold_cap(data: pd.Series, threshold_low: int = 1, threshold_high: int = 5) -> pd.Series:
    """
        Percentile cap

        Parameters:
            data (Series): Input Data
            threshold_low (int, default=1): Lower threshold
            threshold_high (int, default=5): Higher threshold
        Returns:
            data (Series):  Transformed Data
    """
    data_copy = data.copy()
    data_copy[data_copy < threshold_low] = threshold_low
    data_copy[data_copy > threshold_high] = threshold_high
    return data_copy


def percentile_cap(data: pd.Series, percentile_low: int = 5, percentile_high: int = 95) -> pd.Series:
    """
        Percentile cap

        Parameters:
            data (Series): Input Data
            percentile_low (int, default=5): Lower threshold cap
            percentile_high (int, default=95): Higher threshold cap
        Returns:
            data (Series):  Transformed Data
    """
    threshold_low = np.percentile(data, percentile_low)
    threshold_high = np.percentile(data, percentile_high)
    return threshold_cap(data, threshold_low, threshold_high)


def zscore_cap(data: pd.Series, zscore_low: float = 0.1, zscore_high: float = 5) -> pd.Series:
    """
        Z-Score Cap.

        Parameters:
            data (Series): Input Data
            zscore_low (int, default=0.1): Lower zscore cap
            zscore_high (int, default=5): Higher zscore cap
        Returns:
            data (Series):  Transformed Data
    """
    threshold_low = (zscore_low * data.std()) + data.mean()
    threshold_high = (zscore_high * data.std()) + data.mean()
    return threshold_cap(data, threshold_low, threshold_high)


def threshold_binary(data: pd.Series, threshold: float = 5) -> pd.Series:
    """
        Binary data for threshold value.

        Parameters:
            data (Series): Input Data
            threshold (float, default=5): Threshold for flag
        Returns:
            data (Series):  Transformed Data
    """
    return (data > threshold).map({True: 1, False: 0})


def mod(data: pd.Series, mod_value: int = 10) -> pd.Series:
    """
        Binary data for threshold value.

        Parameters:
            data (Series): Input Data
            mod_value (int, default=10): Base of mod operation
        Returns:
            data (Series):  Transformed Data
    """
    return data.mod(mod_value)


if __name__ == "__main__":
    csv_path = "./test.csv"
    data = pd.read_csv(csv_path)
    data = data.dropna()
    print(data.describe())
    data["ln"] = ln(data=data['10YTY_Q_Q_percentage'])
    data["exp"] = exp(data=data['10YTY_Q_Q_percentage'])
    data["square"] = square(data=data['10YTY_Q_Q_percentage'])
    data["sqrt"] = square_root(data=data['10YTY_Q_Q_percentage'])
    data["inverse"] = inverse(data=data['10YTY_Q_Q_percentage'])
    data["X^3"] = power(data=data['10YTY_Q_Q_percentage'])
    data["1/X^3"] = one_over_power(data=data['10YTY_Q_Q_percentage'])
    data["log10"] = log10(data=data['10YTY_Q_Q_percentage'])
    data["log2"] = log2(data=data['10YTY_Q_Q_percentage'])
    data["1/(1-X)"] = one_over_one_minus_x(data=data['10YTY_Q_Q_percentage'])
    data["1/(1+X)"] = one_over_one_plus_x(data=data['10YTY_Q_Q_percentage'])
    data["1/(X-1)"] = one_over_x_minus_one(data=data['10YTY_Q_Q_percentage'])
    data["threshold_cap"] = threshold_cap(data=data['10YTY_Q_Q_percentage'])
    data["percentile_cap"] = percentile_cap(data=data['10YTY_Q_Q_percentage'])
    data["zscore_cap"] = zscore_cap(data=data['10YTY_Q_Q_percentage'])
    data["threshold_binary"] = threshold_binary(data=data['10YTY_Q_Q_percentage'])
    data["mod"] = mod(data=data['10YTY_Q_Q_percentage'])
    print(data.describe())