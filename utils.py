import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_excel("data/dataset.xlsx")


def report(df):
    return df.describe()


# ТЕКСТОВЫЙ ОТЧЕТ
# Отчет 1
def clients_by_income_and_age(df, inc_min, inc_max, age_max, rep=False):
    """
    Фильтрация клиентов по уровню дохода и возрасту

    Parameters
    ----------
    df : DataFrame
        Таблица с данными о клиентах.
    inc_min : int or float
        Минимальное значение дохода.
    inc_max : int or float
        Максимальное значение дохода.
    age_max : int
        Максимальный возраст клиента.
    length : bool, optional
        Если True возвращает количество подходящих записей. По умолчанию False.

    Returns
    -------
    DataFrame or int
        Таблица с отобранными клиентами или количество записей.
    """

    sel = (
        (df['person_income'] >= inc_min) &
        (df['person_income'] <= inc_max) &
        (df['person_age'] <= age_max)
    )

    if not rep:
        return df.loc[sel, [
            'person_age',
            'person_income',
            'loan_amnt',
            'loan_status'
            ]]

    return report(df.loc[sel, [
        'person_age',
        'person_income',
        'loan_amnt',
        'loan_status'
        ]])
    

# Отчет 2
def loan_intents_by_education(df, education_level, rep=False):
    """
    Цели кредита для выбранного уровня образования

    Parameters
    ----------
    df : DataFrame
        Таблица с данными о клиентах.
    education_level : str
        Уровень образования клиента.
    length : bool, optional
        Если True возвращает количество подходящих записей. По умолчанию False.

    Returns
    -------
    DataFrame or int
        Таблица с целями кредита или количество записей.
    """

    sel = df['person_education'] == education_level

    if not rep:
        return df.loc[sel, ['person_education', 'loan_intent', 'loan_amnt']]

    return report(df.loc[sel, ['person_education', 'loan_intent', 'loan_amnt']])


# Отчет 3
def loans_by_interest_range(df, rate_min, rate_max, rep=False):
    """
    Кредиты в заданном диапазоне процентных ставок

    Parameters
    ----------
    df : DataFrame
        Таблица с данными о клиентах.
    rate_min : float
        Минимальная процентная ставка.
    rate_max : float
        Максимальная процентная ставка.
    length : bool, optional
        Если True возвращает количество подходящих записей. По умолчанию False.

    Returns
    -------
    DataFrame or int
        Таблица с выбранными кредитами или количество записей.
    """

    sel = (df['loan_int_rate'] >= rate_min) & (df['loan_int_rate'] <= rate_max)

    if not rep:
        return df.loc[sel, [
                'loan_amnt',
                'loan_int_rate',
                'loan_status',
                'credit_score']
            ]

    return report(df.loc[sel, [
        'loan_amnt',
        'loan_int_rate',
        'loan_status',
        'credit_score']
        ])
    
    
# Отчет 4: Сводная таблица
def pivot_avg_loan(df):
    """
    Сводная таблица: средний размер кредита по образованию и статусу

    Parameters
    ----------
    df : DataFrame
        Таблица с данными о клиентах.

    Returns
    -------
    DataFrame
        Сводная таблица со средними значениями кредита.
    """

    return pd.pivot_table(
        df,
        index='person_education',
        columns='loan_status',
        values='loan_amnt',
        aggfunc='mean',
        fill_value=0
    )
    
    
# ГРАФИЧЕСКИЙ ОТЧЕТ
TARGET = "loan_status"

object_cols = list(df.select_dtypes(include=[np.object_]).columns)
num_cols = list(df.select_dtypes(include=[np.number]).columns)
num_cols.remove(TARGET)


# Папка для сохранения графиков
SAVE_DIR = "data"
os.makedirs(SAVE_DIR, exist_ok=True)

TARGET = "loan_status"


def save_plot(filename):
    """
    Сохраняет текущий график

    Parameters
    ----------
    filename : str
        Имя файла для сохранения графика (включая расширение .png).

    Returns
    -------
    None
    """
    filepath = os.path.join(SAVE_DIR, filename)
    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()


def plot_bar_count(df, column, save=False, filename=None):
    """
    Распределение категориальных фичей

    Parameters
    ----------
    df : DataFrame
        Таблица с данными.
    column : str
        Название категориальной переменной.
    save : bool, optional
        Сохранять ли график в файл. По умолчанию False.
    filename : str, optional
        Имя файла для сохранения. По умолчанию None.

    Returns
    -------
    None
    """
    plt.figure(figsize=(12, 6))
    x = df[column].value_counts().index
    y = df[column].value_counts().values
    sns.barplot(x=x, y=y)
    plt.title(f"Распределение {column}")
    plt.xticks(rotation=45)
    if save:
        filename = filename or f"{column}_dist.png"
        save_plot(filename)
    else:
        plt.show()
        
        
def plot_histogram(df, column, save=False, filename=None):
    """
    Распределение числовых фичей

    Parameters
    ----------
    df : DataFrame
        Таблица с данными.
    column : str
        Название числовой переменной.
    save : bool, optional
        Сохранять ли график в файл. По умолчанию False.
    filename : str, optional
        Имя файла для сохранения. По умолчанию None.

    Returns
    -------
    None
    """
    plt.figure(figsize=(12, 6))
    sns.histplot(df[column], bins=50, kde=True)
    plt.title(f"Распределение {column}")
    if save:
        filename = filename or f"{column}_dist.png"
        save_plot(filename)
    else:
        plt.show()
        
        
def plot_kde(df, column, save=False, filename=None):
    """
    Распределение числовых фичей по таргету

    Parameters
    ----------
    df : DataFrame
        Таблица с данными.
    column : str
        Название числовой переменной.
    save : bool, optional
        Сохранять ли график в файл. По умолчанию False.
    filename : str, optional
        Имя файла для сохранения. По умолчанию None.

    Returns
    -------
    None
    """
    plt.figure(figsize=(12, 6))
    sns.kdeplot(data=df, x=column, hue=TARGET, fill=True)
    plt.title(f"Распределение {column} по {TARGET}")
    if save:
        filename = filename or f"{column}_dist_by_target.png"
        save_plot(filename)
    else:
        plt.show()
        
        
def plot_boxplot(df, column, showfliers=True, save=False, filename=None):
    """
    Boxplot числовых фичей по таргету

    Parameters
    ----------
    df : DataFrame
        Таблица с данными.
    column : str
        Название числовой переменной.
    showfliers : bool, optional
        Отображать ли выбросы. По умолчанию True.
    save : bool, optional
        Сохранять ли график в файл. По умолчанию False.
    filename : str, optional
        Имя файла для сохранения. По умолчанию None.

    Returns
    -------
    None
    """
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x=column, hue=TARGET, showfliers=showfliers)
    plt.title(f"Boxplot {column} по {TARGET}")
    if save:
        filename = filename or f"{column}_box.png"
        save_plot(filename)
    else:
        plt.show()
        
        
def plot_count_by_target(df, column, save=False, filename=None):
    """
    Распределение категориальных фичей по TARGET

    Parameters
    ----------
    df : DataFrame
        Таблица с данными.
    column : str
        Название категориальной переменной.
    save : bool, optional
        Сохранять ли график в файл. По умолчанию False.
    filename : str, optional
        Имя файла для сохранения. По умолчанию None.

    Returns
    -------
    None
    """
    plt.figure(figsize=(12, 6))
    sns.countplot(x=column, hue=TARGET, data=df)
    plt.title(f"Распределение {column} по {TARGET}")
    plt.xticks(rotation=45)
    if save:
        filename = filename or f"{column}_dist_by_target.png"
        save_plot(filename)
    else:
        plt.show()
        
        
def plot_scatter(df, x_col, y_col, save=False, filename=None):
    """
    Зависимость между двумя числовыми фичами

    Parameters
    ----------
    df : DataFrame
        Таблица с данными.
    x_col : str
        Название переменной по оси X.
    y_col : str
        Название переменной по оси Y.
    save : bool, optional
        Сохранять ли график в файл. По умолчанию False.
    filename : str, optional
        Имя файла для сохранения. По умолчанию None.

    Returns
    -------
    None
    """
    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=df, x=x_col, y=y_col, hue=TARGET)
    plt.title(f"Зависимость {y_col} и {x_col}")
    if save:
        filename = filename or f"{y_col}_{x_col}_scatter.png"
        save_plot(filename)
    else:
        plt.show()
        
        
def plot_corr_heatmap(df, save=False, filename="heatmap.png"):
    """
    Тепловая карта корреляций числовых фичей

    Parameters
    ----------
    df : DataFrame
        Таблица с данными.
    save : bool, optional
        Сохранять ли график в файл. По умолчанию False.
    filename : str, optional
        Имя файла для сохранения. По умолчанию "heatmap.png".

    Returns
    -------
    None
    """
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if TARGET in num_cols:
        num_cols.remove(TARGET)

    plt.figure(figsize=(12, 10))
    sns.heatmap(
        df[num_cols].corr(),
        cmap="crest",
        fmt=".2f",
        linewidths=2,
        annot=True
    )
    plt.title("Тепловая карта корреляций")
    if save:
        save_plot(filename)
    else:
        plt.show()