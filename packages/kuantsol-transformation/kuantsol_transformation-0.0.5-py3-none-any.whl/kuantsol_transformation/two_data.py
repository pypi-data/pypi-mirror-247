import pandas as pd


def multiply(data_1: pd.Series, data_2: pd.Series) -> pd.Series:
    """
        data_1 * data_2.

        Parameters:
            data (Series): Input Data
        Returns:
            data (Series):  Transformed Data
    """
    return data_1 * data_2


def divide(data_1: pd.Series, data_2: pd.Series) -> pd.Series:
    """
        data_1 / data_2.

        Parameters:
            data (Series): Input Data
        Returns:
            data (Series):  Transformed Data
    """
    return data_1 / data_2


def add(data_1: pd.Series, data_2: pd.Series) -> pd.Series:
    """
        data_1 + data_2.

        Parameters:
            data (Series): Input Data
        Returns:
            data (Series):  Transformed Data
    """
    return data_1 + data_2


def subtract(data_1: pd.Series, data_2: pd.Series) -> pd.Series:
    """
        data_1 - data_2.

        Parameters:
            data (Series): Input Data
        Returns:
            data (Series):  Transformed Data
    """
    return data_1 - data_2


if __name__ == "__main__":
    csv_path = "./test.csv"
    data = pd.read_csv(csv_path)
    data = data.dropna()
    print(data.describe())
    data["multiply"] = multiply(data_1=data['10YTY_Q_Q_percentage'], data_2=data['Charge_off_Credit_Cards'])
    data["divide"] = divide(data_1=data['10YTY_Q_Q_percentage'], data_2=data['Charge_off_Credit_Cards'])
    data["add"] = add(data_1=data['10YTY_Q_Q_percentage'], data_2=data['Charge_off_Credit_Cards'])
    data["subtract"] = subtract(data_1=data['10YTY_Q_Q_percentage'], data_2=data['Charge_off_Credit_Cards'])
    print(data.describe())