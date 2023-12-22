import numpy as np
import pandas as pd


def RSI(data: pd.Series, period: int = 7) -> pd.Series:
    """
        Calculate RSI indicator in a given period.

        Parameters:
            data (Series): Input data
            period (int, default = 7): Calculation period
        Returns:
            transformed_data (Series):  Transformed Data
    """
    diff = data.diff(1)
    up = diff.where(diff > 0, 0.0)
    dn = -diff.where(diff < 0, 0.0)
    emaup = up.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    emadn = dn.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs = emaup / emadn
    return pd.Series(np.where(emadn == 0, 100, 100 - (100 / (1 + rs))), index=data.index)


def ROC(data: pd.Series, period: int = 7) -> pd.Series:
    """
        Calculate ROC indicator in a given period.

        Parameters:
            data (Series): Input data
            period (int, default = 7): Calculation period
        Returns:
            transformed_data (Series):  Transformed Data
    """
    return ((data - data.shift(period)) / data.shift(period)) * 100


def MACD(data: pd.Series, period_fast: int = 12, period_slow: int = 26) -> pd.Series:
    """
        Calculate MACD indicator in a given period.

        Parameters:
            data (Series): Input data
            period_fast (int, default = 12): Fast period
            period_slow (int, default = 26): Slow period
        Returns:
            transformed_data (Series):  Transformed Data
    """

    emafast = data.ewm(span=period_fast, min_periods=period_fast, adjust=False).mean()
    emaslow = data.ewm(span=period_slow, min_periods=period_slow, adjust=False).mean()
    return emafast - emaslow


def TRIX(data: pd.Series, period: int = 7) -> pd.Series:
    """
        Calculate TRIX indicator in a given period.

        Parameters:
            data (Series): Input data
            period (int, default = 7): Calculation period
        Returns:
            transformed_data (Series):  Transformed Data
    """

    ema1 = data.ewm(span=period, min_periods=period, adjust=False).mean()
    ema2 = ema1.ewm(span=period, min_periods=period, adjust=False).mean()
    ema3 = ema2.ewm(span=period, min_periods=period, adjust=False).mean()
    trix = (ema3 - ema3.shift(1)) / ema3.shift(1)
    trix *= 100
    return trix


def bollinger_upper(data: pd.Series, period: int = 7) -> pd.Series:
    """
        Calculate Bollinger Upper in a given period.

        Parameters:
            data (Series): Input data
            period (int, default = 7): Calculation period
        Returns:
            transformed_data (Series):  Transformed Data
    """

    ma = data.rolling(period, min_periods=1).apply(np.nanmean)
    std = data.rolling(period, min_periods=1).apply(np.nanstd)
    return ma + (2 * std)


def bollinger_lower(data: pd.Series, period: int = 7) -> pd.Series:
    """
        Calculate Bollinger Lower in a given period.

        Parameters:
            data (Series): Input data
            period (int, default = 7): Calculation period
        Returns:
            transformed_data (Series):  Transformed Data
    """

    ma = data.rolling(period, min_periods=1).apply(np.nanmean)
    std = data.rolling(period, min_periods=1).apply(np.nanstd)
    return ma - (2 * std)


def bollinger_band(data: pd.Series, period: int = 7) -> pd.Series:
    """
        Calculate Bollinger Band in a given period.

        Parameters:
            data (Series): Input data
            period (int, default = 7): Calculation period
        Returns:
            transformed_data (Series):  Transformed Data
    """

    ma = data.rolling(period, min_periods=1).apply(np.nanmean)
    std = data.rolling(period, min_periods=1).apply(np.nanstd)
    upper = ma + (2 * std)
    lower = ma - (2 * std)
    return (data - lower) / (upper - lower)


def bias_indicator(data: pd.Series, period: int = 7) -> pd.Series:
    """
        Calculate Bias Indicator in a given period.

        Parameters:
            data (Series): Input data
            period (int, default = 7): Calculation period
        Returns:
            transformed_data (Series):  Transformed Data
    """

    ma = data.rolling(period, min_periods=1).apply(np.nanmean)
    return 100 * (data - ma) / ma


def TSI(data: pd.Series, period_fast: int = 12, period_slow: int = 26) -> pd.Series:
    """
        Calculate TSI Indicator in a given period.

        Parameters:
            data (Series): Input data
            period_fast (int, default = 12): Fast period
            period_slow (int, default = 26): Slow period
        Returns:
            transformed_data (Series):  Transformed Data
    """

    diff_close = data - data.shift(1)
    smoothed = (
        diff_close.ewm(span=period_slow, min_periods=period_slow, adjust=False)
        .mean()
        .ewm(span=period_fast, min_periods=period_fast, adjust=False)
        .mean()
    )
    smoothed_abs = (
        abs(diff_close)
        .ewm(span=period_slow, min_periods=period_slow, adjust=False)
        .mean()
        .ewm(span=period_fast, min_periods=period_fast, adjust=False)
        .mean()
    )
    tsi = smoothed / smoothed_abs
    tsi *= 100
    return tsi


def KAMA(data: pd.Series, period: int = 7, period_fast: int = 12, period_slow: int = 26) -> pd.Series:
    """
        Calculate Kaufman's Adaptive Moving Average in a given period.

        Parameters:
            data (Series): Input data
            period (int, default = 7): Calculation period
            period_fast (int, default = 12): Fast period
            period_slow (int, default = 26): Slow period
        Returns:
            transformed_data (Series):  Transformed Data
    """

    data_values = data.values
    vol = pd.Series(abs(data - np.roll(data, 1)))

    er_num = abs(data_values - np.roll(data_values, period))
    er_den = vol.rolling(period, min_periods=period).sum()
    efficiency_ratio = er_num / er_den

    smoothing_constant = (
            (
                    efficiency_ratio * (2.0 / (period_fast + 1) - 2.0 / (period_slow + 1.0))
                    + 2 / (period_slow + 1.0)
            )
            ** 2.0
    ).values

    kama = np.zeros(smoothing_constant.size)
    len_kama = len(kama)
    first_value = True

    for i in range(len_kama):
        if np.isnan(smoothing_constant[i]):
            kama[i] = np.nan
        elif first_value:
            kama[i] = data_values[i]
            first_value = False
        else:
            kama[i] = kama[i - 1] + smoothing_constant[i] * (data_values[i] - kama[i - 1])
    return kama


def StochRSI(data: pd.Series, period: int = 7) -> pd.Series:
    """
        Calculate StochRSI Indicator in a given period.

        Parameters:
            data (Series): Input data
            period (int, default = 7): Calculation period
        Returns:
            transformed_data (Series):  Transformed Data
    """

    rsi = RSI(data=data, period=period)
    lowest_low_rsi = rsi.rolling(period).min()
    stochrsi = (rsi - lowest_low_rsi) / (rsi.rolling(period).max() - lowest_low_rsi)
    return stochrsi


def PPO(data: pd.Series, period: int = 7, period_fast: int = 12, period_slow: int = 26) -> pd.Series:
    """
        Calculate Percentage Price Oscillator in a given period.

        Parameters:
            data (Series): Input data
            period (int, default = 7): Calculation period
            period_fast (int, default = 12): Fast period
            period_slow (int, default = 26): Slow period
        Returns:
            transformed_data (Series):  Transformed Data
    """

    emafast = data.ewm(span=period_fast, min_periods=period_fast, adjust=False).mean()
    emaslow = data.ewm(span=period_slow, min_periods=period_slow, adjust=False).mean()
    ppo = ((emafast - emaslow) / emaslow) * 100
    return ppo


def Aroon(data: pd.Series, period: int = 7) -> pd.Series:
    """
        Calculate Aroon Indicator in a given period.

        Parameters:
            data (Series): Input data
            period (int, default = 7): Calculation period
        Returns:
            transformed_data (Series):  Transformed Data
    """

    rolling_close = data.rolling(period, min_periods=period)
    aroon_up = rolling_close.apply(lambda x: float(np.argmax(x) + 1) / period * 100, raw=True)
    aroon_down = rolling_close.apply(lambda x: float(np.argmin(x) + 1) / period * 100, raw=True)
    aroon_diff = aroon_up - aroon_down
    return aroon_diff


def WMA(data: pd.Series, period: int = 7) -> pd.Series:
    """
        Calculate Weighted Moving Average Indicator in a given period.

        Parameters:
            data (Series): Input data
            period (int, default = 7): Calculation period
        Returns:
            transformed_data (Series):  Transformed Data
    """

    weight = pd.Series([i * 2 / (period * (period + 1)) for i in range(1, period + 1)])

    def weighted_average(period):
        def _weighted_average(x):
            return (period * x).sum()

        return _weighted_average

    wma = data.rolling(period).apply(weighted_average(period), raw=True)
    return wma


def KST(data: pd.Series, period1: int = 7, period2: int = 14, period3: int = 28, period4: int = 35, roc1: int = 7, roc2: int = 14, roc3: int = 28, roc4: int = 35) -> pd.Series:
    """
        Calculate KST Indicator in a given period.

        Parameters:
            data (Series): Input data
            period1 (int, default = 7): Calculation period1
            period2 (int, default = 14): Calculation period2
            period3 (int, default = 28): Calculation period3
            period4 (int, default = 34): Calculation period4
        Returns:
            transformed_data (Series):  Transformed Data
    """

    rocma1 = (((data - data.shift(roc1, fill_value=data.mean())) / data.shift(roc1, fill_value=data.mean())).rolling(period1, min_periods=period1).mean())
    rocma2 = (((data - data.shift(roc2, fill_value=data.mean())) / data.shift(roc2, fill_value=data.mean())).rolling(period2, min_periods=period2).mean())
    rocma3 = (((data - data.shift(roc3, fill_value=data.mean())) / data.shift(roc3, fill_value=data.mean())).rolling(period3, min_periods=period3).mean())
    rocma4 = (((data - data.shift(roc4, fill_value=data.mean())) / data.shift(roc4, fill_value=data.mean())).rolling(period4, min_periods=period4).mean())
    kst = 100 * (rocma1 + 2 * rocma2 + 3 * rocma3 + 4 * rocma4)
    return kst


def DPO(data: pd.Series, period: int = 7) -> pd.Series:
    """
        Calculate Detrended Price Oscillator in a given period.

        Parameters:
            data (Series): Input data
            period (int, default = 7): Calculation period
        Returns:
            transformed_data (Series):  Transformed Data
    """

    dpo = (data.shift(int((0.5 * period) + 1), fill_value=data.mean())- data.rolling(period, min_periods=period).mean())
    return dpo


def STC(data: pd.Series, period: int = 7, period_fast: int = 12, period_slow: int = 26, smooth1: int = 7, smooth2: int = 14) -> pd.Series:
    """
        Calculate Schaff Trend Cycle in a given period.

        Parameters:
            data (Series): Input data
            period (int, default = 7): Calculation period
            period_fast (int, default = 12): Fast period
            period_slow (int, default = 26): Slow period
            smooth1 (int,default = 7): Ema period over Stoch_k
            smooth2 (int,default = 14): Ema period over Stoch_kd
        Returns:
            transformed_data (Series):  Transformed Data
    """

    emafast = data.ewm(span=period_fast, min_periods=period_fast, adjust=False).mean()
    emaslow = data.ewm(span=period_slow, min_periods=period_slow, adjust=False).mean()
    macd = emafast - emaslow

    macdmin = macd.rolling(window=period).min()
    macdmax = macd.rolling(window=period).max()
    stoch_k = 100 * (macd - macdmin) / (macdmax - macdmin)
    stoch_d = stoch_k.ewm(span=smooth1, min_periods=smooth1, adjust=False).mean()

    stoch_d_min = stoch_d.rolling(window=period).min()
    stoch_d_max = stoch_d.rolling(window=period).max()
    stoch_kd = 100 * (stoch_d - stoch_d_min) / (stoch_d_max - stoch_d_min)
    stc = stoch_kd.ewm(span=smooth2, min_periods=smooth2, adjust=False).mean()
    return stc


if __name__ == "__main__":
    csv_path = "./test.csv"
    data = pd.read_csv(csv_path)
    data = data.dropna()
    print(data.describe())
    data["RSI"] = RSI(data=data['10YTY_Q_Q_percentage'])
    data["ROC"] = ROC(data=data['10YTY_Q_Q_percentage'])
    data["MACD"] = MACD(data=data['10YTY_Q_Q_percentage'])
    data["TRIX"] = TRIX(data=data['10YTY_Q_Q_percentage'])
    data["bollinger_upper"] = bollinger_upper(data=data['10YTY_Q_Q_percentage'])
    data["bollinger_lower"] = bollinger_lower(data=data['10YTY_Q_Q_percentage'])
    data["bollinger_band"] = bollinger_band(data=data['10YTY_Q_Q_percentage'])
    data["bias"] = bias_indicator(data=data['10YTY_Q_Q_percentage'])
    data["TSI"] = TSI(data=data['10YTY_Q_Q_percentage'])
    data["KAMA"] = KAMA(data=data['10YTY_Q_Q_percentage'])
    data["StochRSI"] = StochRSI(data=data['10YTY_Q_Q_percentage'])
    data["PPO"] = PPO(data=data['10YTY_Q_Q_percentage'])
    data["Aroon"] = Aroon(data=data['10YTY_Q_Q_percentage'])
    data["WMA"] = WMA(data=data['10YTY_Q_Q_percentage'])
    data["KST"] = KST(data=data['10YTY_Q_Q_percentage'])
    data["DPO"] = DPO(data=data['10YTY_Q_Q_percentage'])
    data["STC"] = STC(data=data['10YTY_Q_Q_percentage'])
    print(data.describe())