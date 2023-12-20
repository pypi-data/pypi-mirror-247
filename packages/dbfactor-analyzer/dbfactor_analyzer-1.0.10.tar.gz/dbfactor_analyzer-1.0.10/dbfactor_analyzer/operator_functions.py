#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scipy.stats import rankdata
import numpy as np
import pandas as pd


def ts_sum(df, window, center=False):
    """
    移动求和

    参数：
    ------------
    df: DataFrame or Series
    windows: int,窗口大小
    center: bool, 默认False
            是否为中心
    """
    return df.rolling(window,center=center).sum()


def sma(df, window, center=False):
    """
    移动平均

    参数：
    ------------
    df: DataFrame or Series
    windows: int,窗口大小
    center: bool, 默认False
            是否为中心
    
    """
    return df.rolling(window,center=center).mean()


def stddev(df, window,center=False):
    """
    移动标准差

    参数：
    ------------
    df: DataFrame or Series
    windows: int,窗口大小
    center: bool, 默认False
            是否为中心
    
    """   
    return df.rolling(window,center=center).std()


# 移动相关系数
def correlation(x, y, window,center=False):
    """
    移动相关系数

    参数：
    ------------
    x: DataFrame or Series
    y: DataFrame or Series
    windows: int,窗口大小
    center: bool, 默认False
            是否为中心
    
    """  

    return x.rolling(window,center=center).corr(y)


# 移动协方差
def covariance(x, y, window,center=False):
    """
    移动相关系数

    参数：
    ------------
    x: DataFrame or Series
    y: DataFrame or Series
    windows: int,窗口大小
    center: bool, 默认False
            是否为中心
    
    """      
    return x.rolling(window,center=center).cov(y)


def ts_rank(df,window):
    """
    目标值在过去window天的时序排名
    df: DataFrame or Series
    window: int,窗口大小
    
    """
    def rolling_rank(na):
        return rankdata(na)[-1]
    
    return df.rolling(window).apply(rolling_rank)


def product(df, window):
    """
    过去window天的时序乘积
    df: DataFrame or Series
    window: int,窗口大小
    
    """
    def rolling_prod(na):
        return np.prod(na)
    
    return df.rolling(window).apply(rolling_prod)


def ts_min(df, window):
    """
    过去window天的最小值
    df: DataFrame or Series
    window: int,窗口大小
    
    """    
    return df.rolling(window).min()


def ts_max(df, window):
    """
    过去window天的最大值
    df: DataFrame or Series
    window: int,窗口大小
    
    """      
    return df.rolling(window).max()



def delta(df, period):
    """
    当天值减去period天前的值
    df: DataFrame or Series
    period: int
    """
    return df.diff(period)


# d天前的值，滞后值
def delay(df, period):
    """
    底层为shift函数
    df: DataFrame or Series
    period: int    
    """
    return df.shift(period)



def rank_section(df):
    """截面数据百分比排序 """
    return df.rank(pct=True, axis=1)


def normalization(df, k=1):
    """归一化"""
    return df.mul(k).div(np.abs(df).sum())


def ts_argmax(df, window):
    """过去d天最大值的位置 """
    return df.rolling(window).apply(np.argmax) + 1



def ts_argmin(df, window):
    """过去d天最小值的位置"""
    return df.rolling(window).apply(np.argmin) + 1



def decay_linear(df, period):
    """线性衰减的移动平均加权"""
    if df.isnull().values.any():
        #df.fillna(method='ffill', inplace=True)
        #df.fillna(method='bfill', inplace=True)
        df.fillna(value=0, inplace=True)
    na_lwma = np.zeros_like(df)  # 生成与df大小相同的零数组
    na_lwma[:period, :] = df.iloc[:period, :]  # 赋前period项的值
    na_series = df.iloc[:, :].values
    # 计算加权系数
    divisor = period * (period + 1) / 2
    y = (np.arange(period) + 1) * 1.0 / divisor
    # 从第period项开始计算数值
    for row in range(period - 1, df.shape[0]):
        x = na_series[row - period + 1: row + 1, :]
        na_lwma[row, :] = (np.dot(x.T, y))
    return pd.DataFrame(na_lwma, index=df.index, columns=df.columns)


''' 
# 运行太慢了，不如上面的
def decay_linear1(df,period):
    if df.isnull().values.any():
        df.fillna(value=0,inplace=True)
    #计算加权系数
    divisor=period*(period+1)/2
    y=(np.arange(period)+1)*1.0/divisor

    result=df.rolling(period).apply(lambda x: np.dot(x.T,y))
    result.iloc[:period-1,:]=df.iloc[:period-1,:]

    return result

 '''

def VWAP(h,l,v):
    """计算VWAP
    h: 最高价
    l: 最低价
    v: 成交量
    """
    return np.divide((v*(h+l)/2).cumsum(),v.cumsum())
