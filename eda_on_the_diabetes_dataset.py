# -*- coding: utf-8 -*-
"""EDA on the diabetes dataset.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rUhk1wjxjxhYx91HY8piDgJGzj19zhIr

# Exploratory Data Analysis: Diabetes Dataset

# Business Problem

This study aims to perform exploratory data analysis using the diabetes dataset.

# Dataset Story

This dataset is originally from the National Institute of Diabetes and Digestive and Kidney
Diseases. The objective of the dataset is to diagnostically predict whether a patient has diabetes,
based on certain diagnostic measurements included in the dataset. Several constraints were placed
on the selection of these instances from a larger database. In particular, all patients here are females
at least 21 years old of Pima Indian heritage.2
From the data set in the (.csv) File We can find several variables, some of them are independent
(several medical predictor variables) and only one target dependent variable (Outcome).

**Information about dataset attributes**:

***Pregnancies***: To express the Number of pregnancies

***Glucose***: To express the Glucose level in blood

***BloodPressure***: To express the Blood pressure measurement

***SkinThickness***: To express the thickness of the skin

***Insulin***: To express the Insulin level in blood

***BMI***: To express the Body mass index

***DiabetesPedigreeFunction***: To express the Diabetes percentage

***Age***: To express the age

***Outcome***: To express the final result 1 is Yes and 0 is No

# Import Necessary Libraries
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math
import io

# Settings
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 500)
pd.set_option("display.float_format", lambda x: "%.3f" % x)

"""# Import Dataset"""

df = pd.read_csv('https://raw.githubusercontent.com/Humphrey-Galiwango99/MCS-7103-EDA-Assignment/main/diabetes.csv')
print(df.head())

"""# General Information About to Dataset"""

def check_df(dataframe, head=5):
    print(20*"#", "Head", 20*"#")
    print(dataframe.head(head))
    print(20*"#", "Tail", 20*"#")
    print(dataframe.tail(head))
    print(20*"#", "Shape", 20*"#")
    print(dataframe.shape)
    print(20*"#", "Type", 20*"#")
    print(dataframe.dtypes)
    print(20*"#", "NA", 20*"#")
    print(dataframe.isnull().sum())
    print(20*"#", "Quartiles", 20*"#")
    print(dataframe.describe([0, 0.01, 0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.99, 1]).T)

check_df(df)

"""# Analysis of Categorical and Numerical Columns"""

def grab_col_names(dataframe, cat_th=10, car_th=20, report=False):
    # categorical
    cat_cols = [col for col in dataframe.columns if str(dataframe[col].dtypes) in ["category", "object", "bool"]]
    num_but_cat = [col for col in dataframe.columns if dataframe[col].nunique()<cat_th and str(dataframe[col].dtypes) in ["int64", "float64", "uint8"]]
    cat_but_car = [col for col in dataframe.columns if dataframe[col].nunique()>car_th and str(dataframe[col].dtypes) in ["category", "object"]]
    cat_cols = num_but_cat + cat_cols
    cat_cols = [col for col in cat_cols if col not in cat_but_car]
    # numerical
    num_cols = [col for col in dataframe.columns if str(dataframe[col].dtypes) in ["int64", "float64", "uint8"] and col not in cat_cols]

    if report:
        print(f"Observation: {df.shape[0]}")
        print(f"Variables: {df.shape[1]}")
        print(f"Cat Cols: {len(cat_cols)}")
        print(f"Num Cols: {len(num_cols)}")
        print(f"Cat But Car Cols: {len(cat_but_car)}")
        print(f"Num but Cat Cols: {len(num_but_cat)}")

    return cat_cols, num_cols, cat_but_car, num_but_cat

cat_cols, num_cols, cat_but_car, num_but_cat = grab_col_names(df, report=True)

def cat_summary(dataframe, col_name, plot=False):
    print(20*"#",col_name,20*"#")
    print(pd.DataFrame({col_name: dataframe[col_name].value_counts(),
                 "Ratio":100* dataframe[col_name].value_counts()/ len(dataframe)}))

    if plot:
        sns.countplot(x=dataframe[col_name], data=dataframe)
        plt.show(block=True)

def cat_summary_df(dataframe):
    cat_cols, num_cols, cat_but_car, num_but_cat = grab_col_names(dataframe)
    for col in cat_cols:
        if str(df[col].dtypes) == "bool":
            new_df = pd.DataFrame()
            new_df[col] = dataframe[col].astype(int)
            cat_summary(new_df, col, plot=True)
        else:
            cat_summary(dataframe, col, plot=True)

cat_summary_df(df)

def num_summary(dataframe, num_col, plot=False):
    print(20*"#", num_col, 20*"#")
    quartiles = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99]
    print(dataframe[num_col].describe(quartiles).T)

    if plot:
        dataframe[num_col].hist(bins=20)
        plt.xlabel(num_col)
        plt.title(num_col)
        plt.show(block=True)

def num_summary_df(dataframe):
    cat_cols, num_cols, cat_but_car, num_but_cat = grab_col_names(dataframe)
    for col in num_cols:
        num_summary(dataframe, col, plot=True)

num_summary_df(df)

def plot_num_summary(dataframe):
    cat_cols, num_cols, cat_but_car, num_but_cat = grab_col_names(dataframe)
    num_plots = len(num_cols)
    rows = math.ceil(num_plots/2)
    cols = 2 if num_plots > 1 else 1
    plt.figure(figsize=(10*cols,4*rows))
    for index, col in enumerate(num_cols):
        plt.subplot(rows, cols, index+1)
        plt.tight_layout()
        dataframe[col].hist(bins=20)
        plt.title(col)

plot_num_summary(df)

"""# Target Analysis"""

def target_summary_with_num(dataframe, target, numerical_col):
    print(20*"#", target, "==>", numerical_col, 20*"#")
    print(pd.DataFrame({"Target Mean": dataframe.groupby(target)[numerical_col].mean()}))

def target_summary_with_num_df(dataframe, target):
    cat_cols, num_cols, cat_but_car, num_but_cat = grab_col_names(dataframe)
    for col in num_cols:
        target_summary_with_num(dataframe, target, col)

target_summary_with_num_df(df, "Outcome")

"""# Correlation Analysis"""

def high_corralated_cols(dataframe, corr_th=0.90, plot=False, remove=False):
    num_cols = [col for col in dataframe.columns if str(dataframe[col].dtypes) in ["int64", "float64", "uint8"]]
    corr = dataframe[num_cols].corr()
    corr_matrix = corr.abs()
    upper_triangle_matrix = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    drop_list = [col for col in upper_triangle_matrix.columns if any(upper_triangle_matrix[col] > corr_th)]
    if drop_list == []:
        print(20*"#", "After Correlation Anlysis, You Don't Need to Remove Variables", 20*"#")
    if remove:
        dataframe = dataframe.drop(drop_list, axis=1)
        num_cols = [col for col in dataframe.columns if str(dataframe[col].dtypes) in ["int64", "float64", "uint8"]]
    if plot:
        sns.set(rc={'figure.figsize': (6,3)})
        sns.heatmap(dataframe[num_cols].corr(), cmap="RdBu", annot=True, fmt=".2f")
        plt.show(block=True)

    return drop_list

drop_list = high_corralated_cols(df, plot=True, remove=True)

