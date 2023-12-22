import numpy as np
import pandas as pd
import statsmodels.api as sm


def pctChange(data: pd.Series, period: int = 7) -> pd.Series:
    """
        Pct change of data in given period.

        Parameters:
            data (Series): Input Data
            period (int, default=7): Period of pct change calculation
        Returns:
            data (Series):  Transformed Data
    """
    return data.pct_change(period)


def difference(data: pd.Series) -> pd.Series:
    """
        First discrete difference of given data.

        Parameters:
            data (Series): Input Data
        Returns:
            data (Series):  Transformed Data
    """
    return data.diff()


def lag(data: pd.Series, period: int = 1) -> pd.Series:
    """
        Shift the data by a given period.

        Parameters:
            data (Series): Input Data
            period (int, default=1): Period of lag
        Returns:
            data (Series):  Transformed Data
    """
    return data.shift(period)


def moving_average(data: pd.Series, period: int = 7) -> pd.Series:
    """
        Moving average of data in given period.

        Parameters:
            data (Series): Input Data
            period (int, default=7): Period of lag
        Returns:
            data (Series):  Transformed Data
    """
    return data.rolling(period).mean()


def seasonal_decompose(data: pd.Series, period: int = 7) -> pd.Series:
    """
        Seasonal decomposition using moving averages.

        Parameters:
            data (Series): Input Data
            period (int, default=7): Period of time windows
        Returns:
            data (Series):  Transformed Data
    """
    return sm.tsa.seasonal_decompose(data, period=period)


def std_rolling(data: pd.Series, period: int = 7) -> pd.Series:
    """
        Rolling standard deviation in a given period.

        Parameters:
            data (Series): Input Data
            period (int, default=7): Period of time windows
        Returns:
            data (Series):  Transformed Data
    """
    return data.rolling(period, min_periods=1).apply(np.nanstd)


def stdovermean_rolling(data: pd.Series, period: int = 7) -> pd.Series:
    """
        Rolling standard deviation over mean in a given period.

        Parameters:
            data (Series): Input Data
            period (int, default=7): Period of time windows
        Returns:
            data (Series):  Transformed Data
    """
    std_data = data.rolling(period, min_periods=1).apply(np.nanstd)
    mean_data = data.rolling(period, min_periods=1).apply(np.nanmean)
    return std_data / mean_data


def relation_to_last(data: pd.Series, period: int = 7) -> pd.Series:
    """
        Rolling relation to last.

        Parameters:
            data (Series): Input Data
            period (int, default=7): Period of time windows
        Returns:
            data (Series):  Transformed Data
    """
    data_rolling_mean = data.rolling(period, min_periods=1).apply(np.nanmean)
    return data / data_rolling_mean


def exponential_moving_avg(data: pd.Series, period: int = 7) -> pd.Series:
    """
        Exponential moving average in a given period.

        Parameters:
            data (Series): Input Data
            period (int, default=7): Period of time windows
        Returns:
            data (Series):  Transformed Data
    """
    return data.ewm(ignore_na=True, span=period, min_periods=1).mean()


def x_minus_lagx_divide_x(data: pd.Series, period: int = 1) -> pd.Series:
    """
        (X-LagX)/X

        Parameters:
            data (Series): Input Data
            period (int, default=1): Period of lag
        Returns:
            data (Series):  Transformed Data
    """
    return (data - lag(data, period)) / data


def x_minus_lagx_divide_lagx(data: pd.Series, period: int = 1) -> pd.Series:
    """
        (X-LagX)/LagX

        Parameters:
            data (Series): Input Data
            period (int, default=1): Period of lag
        Returns:
            data (Series):  Transformed Data
    """
    return (data - lag(data, period)) / lag(data, period)


def x_minus_lagx(data: pd.Series, period: int = 1) -> pd.Series:
    """
        X-LagX

        Parameters:
            data (Series): Input Data
            period (int, default=1): Period of lag
        Returns:
            data (Series):  Transformed Data
    """
    return data - lag(data, period)


if __name__ == "__main__":
    csv_path = "./test.csv"
    data = pd.read_csv(csv_path)
    data = data.dropna()
    print(data.describe())
    data["pctChange"] = pctChange(data=data['10YTY_Q_Q_percentage'])
    data["diff"] = difference(data=data['10YTY_Q_Q_percentage'])
    data["lag"] = lag(data=data['10YTY_Q_Q_percentage'])
    data["moving_avg"] = moving_average(data=data['10YTY_Q_Q_percentage'])
    data["seasonal_decompose"] = seasonal_decompose(data=data['10YTY_Q_Q_percentage'])
    data["std_rolling"] = std_rolling(data=data['10YTY_Q_Q_percentage'])
    data["stdovermean_rolling"] = stdovermean_rolling(data=data['10YTY_Q_Q_percentage'])
    data["relation_to_last"] = relation_to_last(data=data['10YTY_Q_Q_percentage'])
    data["exponential_moving_avg"] = exponential_moving_avg(data=data['10YTY_Q_Q_percentage'])
    data["exponential_moving_avg"] = exponential_moving_avg(data=data['10YTY_Q_Q_percentage'])
    data["(X-LagX)/X"] = x_minus_lagx_divide_x(data=data['10YTY_Q_Q_percentage'])
    data["(X-LagX)/LagX"] = x_minus_lagx_divide_lagx(data=data['10YTY_Q_Q_percentage'])
    data["X-LagX"] = x_minus_lagx(data=data['10YTY_Q_Q_percentage'])
    print(data.describe())