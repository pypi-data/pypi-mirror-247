#!/usr/bin/env python

# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import statsmodels.api as sm

from . import operator_functions as op

def alpha1(close, returns):
    x = close
    x[returns < 0] = op.stddev(returns, 20)
    alpha = op.rank(op.ts_argmax(x ** 2, 5)) - 0.5
    return alpha.fillna(value=0)


def alpha2(Open, close, volume):
    r1 = op.rank(op.delta(np.log(volume), 2))
    r2 = op.rank((close - Open) / Open)
    alpha = -1 * op.correlation(r1, r2, 6)
    return alpha.fillna(value=0)


def alpha3(Open, volume):
    r1 = op.rank(Open)
    r2 = op.rank(volume)
    alpha = -1 * op.correlation(r1, r2, 10)
    return alpha.replace([-np.inf, np.inf], 0).fillna(value=0)


def alpha4(low):
    r = op.rank(low)
    alpha = -1 * op.ts_rank(r, 9)
    return alpha.fillna(value=0)


def alpha5(Open, vwap, close):
    alpha = (op.rank((Open - (op.ts_sum(vwap, 10) / 10))) * (-1 * abs(op.rank((close - vwap)))))
    return alpha.fillna(value=0)


def alpha6(Open, volume):
    alpha = -1 * op.correlation(Open, volume, 10)
    return alpha.replace([-np.inf, np.inf], 0).fillna(value=0)


def alpha7(volume, close):
    adv20 = op.sma(volume, 20)
    alpha = -1 * op.ts_rank(abs(op.delta(close, 7)), 60) * np.sign(op.delta(close, 7))
    alpha[adv20 >= volume] = -1
    return alpha.fillna(value=0)


def alpha8(Open, returns):
    x1 = (op.ts_sum(Open, 5) * op.ts_sum(returns, 5))
    x2 = op.delay((op.ts_sum(Open, 5) * op.ts_sum(returns, 5)), 10)
    alpha = -1 * op.rank(x1 - x2)
    return alpha.fillna(value=0)


def alpha9(close):
    op.delta_close = op.delta(close, 1)
    x1 = op.ts_min(op.delta_close, 5) > 0
    x2 = op.ts_max(op.delta_close, 5) < 0
    alpha = -1 * op.delta_close
    alpha[x1 | x2] = op.delta_close
    return alpha.fillna(value=0)


def alpha10(close):
    op.delta_close = op.delta(close, 1)
    x1 = op.ts_min(op.delta_close, 4) > 0
    x2 = op.ts_max(op.delta_close, 4) < 0
    x = -1 * op.delta_close
    x[x1 | x2] = op.delta_close
    alpha = op.rank(x)
    return alpha.fillna(value=0)


def alpha11(vwap, close, volume):
    x1 = op.rank(op.ts_max((vwap - close), 3))
    x2 = op.rank(op.ts_min((vwap - close), 3))
    x3 = op.rank(op.delta(volume, 3))
    alpha = (x1 + x2) * x3
    return alpha.fillna(value=0)


def alpha12(volume, close):
    alpha = np.sign(op.delta(volume, 1)) * (-1 * op.delta(close, 1))
    return alpha.fillna(value=0)


def alpha13(volume, close):
    alpha = -1 * op.rank(op.covariance(op.rank(close), op.rank(volume), 5))
    return alpha.fillna(value=0)


def alpha14(Open, volume, returns):
    x1 = op.correlation(Open, volume, 10).replace([-np.inf, np.inf], 0).fillna(value=0)
    x2 = -1 * op.rank(op.delta(returns, 3))
    alpha = x1 * x2
    return alpha.fillna(value=0)


def alpha15(high, volume):
    x1 = op.correlation(op.rank(high), op.rank(volume), 3).replace([-np.inf, np.inf], 0).fillna(value=0)
    alpha = -1 * op.ts_sum(op.rank(x1), 3)
    return alpha.fillna(value=0)


def alpha16(high, volume):
    alpha = -1 * op.rank(op.covariance(op.rank(high), op.rank(volume), 5))
    return alpha.fillna(value=0)


def alpha17(volume, close):
    adv20 = op.sma(volume, 20)
    x1 = op.rank(op.ts_rank(close, 10))
    x2 = op.rank(op.delta(op.delta(close, 1), 1))
    x3 = op.rank(op.ts_rank((volume / adv20), 5))
    alpha = -1 * (x1 * x2 * x3)
    return alpha.fillna(value=0)


def alpha18(close, Open):
    x = op.correlation(close, Open, 10).replace([-np.inf, np.inf], 0).fillna(value=0)
    alpha = -1 * (op.rank((op.stddev(abs((close - Open)), 5) + (close - Open)) + x))
    return alpha.fillna(value=0)


def alpha19(close, returns):
    x1 = (-1 * np.sign((close - op.delay(close, 7)) + op.delta(close, 7)))
    x2 = (1 + op.rank(1 + op.ts_sum(returns, 250)))
    alpha = x1 * x2
    return alpha.fillna(value=0)


def alpha20(Open, high, close, low):
    alpha = -1 * (op.rank(Open - op.delay(high, 1)) * op.rank(Open - op.delay(close, 1)) * op.rank(Open - op.delay(low, 1)))
    return alpha.fillna(value=0)


def alpha21(volume, close):
    x1 = op.sma(close, 8) + op.stddev(close, 8) < op.sma(close, 2)
    x2 = op.sma(close, 8) - op.stddev(close, 8) > op.sma(close, 2)
    x3 = op.sma(volume, 20) / volume < 1
    alpha = pd.DataFrame(np.ones_like(close), index=close.index, columns=close.columns)
    alpha[x1 | x3] = -1 * alpha
    return alpha


def alpha22(high, volume, close):
    x = op.correlation(high, volume, 5).replace([-np.inf, np.inf], 0).fillna(value=0)
    alpha = -1 * op.delta(x, 5) * op.rank(op.stddev(close, 20))
    return alpha.fillna(value=0)


def alpha23(high, close):
    x = op.sma(high, 20) < high
    alpha = pd.DataFrame(np.zeros_like(close), index=close.index, columns=close.columns)
    alpha[x] = -1 * op.delta(high, 2).fillna(value=0)
    return alpha


def alpha24(close):
    x = op.delta(op.sma(close, 100), 100) / op.delay(close, 100) <= 0.05
    alpha = -1 * op.delta(close, 3)
    alpha[x] = -1 * (close - op.ts_min(close, 100))
    return alpha.fillna(value=0)


def alpha25(volume, returns, vwap, high, close):
    adv20 = op.sma(volume, 20)
    alpha = op.rank((((-1 * returns) * adv20) * vwap) * (high - close))
    return alpha.fillna(value=0)


def alpha26(volume, high):
    x = op.correlation(op.ts_rank(volume, 5), op.ts_rank(high, 5), 5).replace([-np.inf, np.inf], 0).fillna(value=0)
    alpha = -1 * op.ts_max(x, 3)
    return alpha.fillna(value=0)


def alpha27(volume, vwap):
    alpha = op.rank((op.sma(op.correlation(op.rank(volume), op.rank(vwap), 6), 2) / 2.0))
    alpha[alpha > 0.5] = -1
    alpha[alpha <= 0.5] = 1
    return alpha.fillna(value=0)


def alpha28(volume, high, low, close):
    adv20 = op.sma(volume, 20)
    x = op.correlation(adv20, low, 5).replace([-np.inf, np.inf], 0).fillna(value=0)
    alpha = op.scale(((x + ((high + low) / 2)) - close))
    return alpha.fillna(value=0)


def alpha29(close, returns):
    x1 = op.ts_min(op.rank(op.rank(op.scale(np.log(op.ts_sum(op.rank(op.rank(-1 * op.rank(op.delta((close - 1), 5)))), 2))))), 5)
    x2 = op.ts_rank(op.delay((-1 * returns), 6), 5)
    alpha = x1 + x2
    return alpha.fillna(value=0)


def alpha30(close, volume):
    op.delta_close = op.delta(close, 1)
    x = np.sign(op.delta_close) + np.sign(op.delay(op.delta_close, 1)) + np.sign(op.delay(op.delta_close, 2))
    alpha = ((1.0 - op.rank(x)) * op.ts_sum(volume, 5)) / op.ts_sum(volume, 20)
    return alpha.fillna(value=0)


def alpha31(close, low, volume):
    adv20 = op.sma(volume, 20)
    x1 = op.rank(op.rank(op.rank(op.decay_linear((-1 * op.rank(op.rank(op.delta(close, 10)))), 10))))
    x2 = op.rank((-1 * op.delta(close, 3)))
    x3 = np.sign(op.scale(op.correlation(adv20, low, 12).replace([-np.inf, np.inf], 0).fillna(value=0)))
    alpha = x1 + x2 + x3
    return alpha.fillna(value=0)


def alpha32(close, vwap):
    x = op.correlation(vwap, op.delay(close, 5), 230).replace([-np.inf, np.inf], 0).fillna(value=0)
    alpha = op.scale(((op.sma(close, 7)) - close)) + 20 * op.scale(x)
    return alpha.fillna(value=0)


def alpha33(Open, close):
    alpha = op.rank(-1 + (Open / close))
    return alpha


def alpha34(close, returns):
    x = (op.stddev(returns, 2) / op.stddev(returns, 5)).fillna(value=0)
    alpha = op.rank(2 - op.rank(x) - op.rank(op.delta(close, 1)))
    return alpha.fillna(value=0)


def alpha35(volume, close, high, low, returns):
    x1 = op.ts_rank(volume, 32)
    x2 = 1 - op.ts_rank(close + high - low, 16)
    x3 = 1 - op.ts_rank(returns, 32)
    alpha = (x1 * x2 * x3).fillna(value=0)
    return alpha


def alpha36(Open, close, volume, returns, vwap):
    adv20 = op.sma(volume, 20)
    x1 = 2.21 * op.rank(op.correlation((close - Open), op.delay(volume, 1), 15))
    x2 = 0.7 * op.rank((Open - close))
    x3 = 0.73 * op.rank(op.ts_rank(op.delay((-1 * returns), 6), 5))
    x4 = op.rank(abs(op.correlation(vwap, adv20, 6)))
    x5 = 0.6 * op.rank((op.sma(close, 200) - Open) * (close - Open))
    alpha = x1 + x2 + x3 + x4 + x5
    return alpha.fillna(value=0)


def alpha37(Open, close):
    alpha = op.rank(op.correlation(op.delay(Open - close, 1), close, 200)) + op.rank(Open - close)
    return alpha


def alpha38(close, Open):
    x = (close / Open).replace([-np.inf, np.inf], 0).fillna(value=0)
    alpha = -1 * op.rank(op.ts_rank(Open, 10)) * op.rank(x)
    return alpha.fillna(value=0)


def alpha39(volume, close, returns):
    adv20 = op.sma(volume, 20)
    x = -1 * op.rank(op.delta(close, 7)) * (1 - op.rank(op.decay_linear((volume / adv20), 9)))
    alpha = x * (1 + op.rank(op.ts_sum(returns, 250)))
    return alpha.fillna(value=0)


def alpha40(high, volume):
    alpha = -1 * op.rank(op.stddev(high, 10)) * op.correlation(high, volume, 10)
    return alpha.fillna(value=0)


def alpha41(high, low, vwap):
    alpha = pow((high * low), 0.5) - vwap
    return alpha


def alpha42(vwap, close):
    alpha = op.rank((vwap - close)) / op.rank((vwap + close))
    return alpha


def alpha43(volume, close):
    adv20 = op.sma(volume, 20)
    alpha = op.ts_rank(volume / adv20, 20) * op.ts_rank((-1 * op.delta(close, 7)), 8)
    return alpha.fillna(value=0)


def alpha44(high, volume):
    alpha = -1 * op.correlation(high, op.rank(volume), 5).replace([-np.inf, np.inf], 0).fillna(value=0)
    return alpha


def alpha45(close, volume):
    x = op.correlation(close, volume, 2).replace([-np.inf, np.inf], 0).fillna(value=0)
    alpha = -1 * (op.rank(op.sma(op.delay(close, 5), 20)) * x * op.rank(op.correlation(op.ts_sum(close, 5), op.ts_sum(close, 20), 2)))
    return alpha.fillna(value=0)


def alpha46(close):
    x = ((op.delay(close, 20) - op.delay(close, 10)) / 10) - ((op.delay(close, 10) - close) / 10)
    alpha = (-1 * (close - op.delay(close, 1)))
    alpha[x < 0] = 1
    alpha[x > 0.25] = -1
    return alpha.fillna(value=0)


def alpha47(volume, close, high, vwap):
    adv20 = op.sma(volume, 20)
    alpha = ((op.rank((1 / close)) * volume) / adv20) * ((high * op.rank((high - close))) / op.sma(high, 5)) - op.rank(
        (vwap - op.delay(vwap, 5)))
    return alpha.fillna(value=0)


def alpha49(close):
    x = (((op.delay(close, 20) - op.delay(close, 10)) / 10) - ((op.delay(close, 10) - close) / 10))
    alpha = (-1 * op.delta(close, 1))
    alpha[x < -0.1] = 1
    return alpha.fillna(value=0)


def alpha50(volume, vwap):
    alpha = -1 * op.ts_max(op.rank(op.correlation(op.rank(volume), op.rank(vwap), 5)), 5)
    return alpha.fillna(value=0)


def alpha51(close):
    inner = (((op.delay(close, 20) - op.delay(close, 10)) / 10) - ((op.delay(close, 10) - close) / 10))
    alpha = (-1 * op.delta(close, 1))
    alpha[inner < -0.05] = 1
    return alpha.fillna(value=0)


def alpha52(returns, volume, low):
    x = op.rank(((op.ts_sum(returns, 240) - op.ts_sum(returns, 20)) / 220))
    alpha = -1 * op.delta(op.ts_min(low, 5), 5) * x * op.ts_rank(volume, 5)
    return alpha.fillna(value=0)


def alpha53(close, high, low):
    alpha = -1 * op.delta((((close - low) - (high - close)) / (close - low).replace(0, 0.0001)), 9)
    return alpha.fillna(value=0)


def alpha54(Open, close, high, low):
    x = (low - high).replace(0, -0.0001)
    alpha = -1 * (low - close) * (Open ** 5) / (x * (close ** 5))
    return alpha


def alpha55(high, low, close, volume):
    x = (close - op.ts_min(low, 12)) / (op.ts_max(high, 12) - op.ts_min(low, 12)).replace(0, 0.0001)
    alpha = -1 * op.correlation(op.rank(x), op.rank(volume), 6).replace([-np.inf, np.inf], 0).fillna(value=0)
    return alpha


def alpha56(returns, cap):
    alpha = 0 - (1 * (op.rank((op.sma(returns, 10) / op.sma(op.sma(returns, 2), 3))) * op.rank((returns * cap))))
    return alpha.fillna(value=0)


def alpha57(close, vwap):
    alpha = 0 - 1 * ((close - vwap) / op.decay_linear(op.rank(op.ts_argmax(close, 30)), 2))
    return alpha.fillna(value=0)


def alpha60(close, high, low, volume):
    x = ((close - low) - (high - close)) * volume / (high - low).replace(0, 0.0001)
    alpha = - ((2 * op.scale(op.rank(x))) - op.scale(op.rank(op.ts_argmax(close, 10))))
    return alpha.fillna(value=0)


def alpha61(volume, vwap):
    adv180 = op.sma(volume, 180)
    alpha = op.rank((vwap - op.ts_min(vwap, 16))) < op.rank(op.correlation(vwap, adv180, 18))
    return alpha


def alpha62(volume, high, low, Open, vwap):
    adv20 = op.sma(volume, 20)
    x1 = op.rank(op.correlation(vwap, op.ts_sum(adv20, 22), 10))
    x2 = op.rank(((op.rank(Open) + op.rank(Open)) < (op.rank(((high + low) / 2)) + op.rank(high))))
    alpha = x1 < x2
    return alpha * -1


def alpha64(high, low, Open, volume, vwap):
    adv120 = op.sma(volume, 120)
    x1 = op.rank(op.correlation(op.ts_sum(((Open * 0.178404) + (low * (1 - 0.178404))), 13), op.ts_sum(adv120, 13), 17))
    x2 = op.rank(op.delta(((((high + low) / 2) * 0.178404) + (vwap * (1 - 0.178404))), 3.69741))
    alpha = x1 < x2
    return alpha * -1


def alpha65(volume, vwap, Open):
    adv60 = op.sma(volume, 60)
    x1 = op.rank(op.correlation(((Open * 0.00817205) + (vwap * (1 - 0.00817205))), op.ts_sum(adv60, 9), 6))
    x2 = op.rank((Open - op.ts_min(Open, 14)))
    alpha = x1 < x2
    return alpha * -1


def alpha66(vwap, low, Open, high):
    x1 = op.rank(op.decay_linear(op.delta(vwap, 4), 7))
    x2 = (((low * 0.96633) + (low * (1 - 0.96633))) - vwap) / (Open - ((high + low) / 2))
    alpha = (x1 + op.ts_rank(op.decay_linear(x2, 11), 7)) * -1
    return alpha.fillna(value=0)


def alpha68(volume, high, close, low):
    adv15 = op.sma(volume, 15)
    x1 = op.ts_rank(op.correlation(op.rank(high), op.rank(adv15), 9), 14)
    x2 = op.rank(op.delta(((close * 0.518371) + (low * (1 - 0.518371))), 1.06157))
    alpha = x1 < x2
    return alpha * -1


def alpha71(volume, close, low, Open, vwap):
    adv180 = op.sma(volume, 180)
    x1 = op.ts_rank(op.decay_linear(op.correlation(op.ts_rank(close, 3), op.ts_rank(adv180, 12), 18), 4), 16)
    x2 = op.ts_rank(op.decay_linear((op.rank(((low + Open) - (vwap + vwap))).pow(2)), 16), 4)
    alpha = x1
    alpha[x1 < x2] = x2
    return alpha.fillna(value=0)


def alpha72(volume, high, low, vwap):
    adv40 = op.sma(volume, 40)
    x1 = op.rank(op.decay_linear(op.correlation(((high + low) / 2), adv40, 9), 10))
    x2 = op.rank(op.decay_linear(op.correlation(op.ts_rank(vwap, 4), op.ts_rank(volume, 19), 7), 3))
    alpha = (x1 / x2.replace(0, 0.0001)).fillna(value=0)
    return alpha


def alpha73(vwap, Open, low):
    x1 = op.rank(op.decay_linear(op.delta(vwap, 5), 3))
    x2 = op.delta(((Open * 0.147155) + (low * (1 - 0.147155))), 2) / ((Open * 0.147155) + (low * (1 - 0.147155)))
    x3 = op.ts_rank(op.decay_linear((x2 * -1), 3), 17)
    alpha = x1
    alpha[x1 < x3] = x3
    return -1 * alpha.fillna(value=0)


def alpha74(volume, close, high, vwap):
    adv30 = op.sma(volume, 30)
    x1 = op.rank(op.correlation(close, op.ts_sum(adv30, 37), 15))
    x2 = op.rank(op.correlation(op.rank(((high * 0.0261661) + (vwap * (1 - 0.0261661)))), op.rank(volume), 11))
    alpha = x1 < x2
    return alpha * -1


def alpha75(volume, vwap, low):
    adv50 = op.sma(volume, 50)
    alpha = op.rank(op.correlation(vwap, volume, 4)) < op.rank(op.correlation(op.rank(low), op.rank(adv50), 12))
    return alpha


def alpha77(volume, high, low, vwap):
    adv40 = op.sma(volume, 40)
    x1 = op.rank(op.decay_linear(((((high + low) / 2) + high) - (vwap + high)), 20))
    x2 = op.rank(op.decay_linear(op.correlation(((high + low) / 2), adv40, 3), 6))
    alpha = x1
    alpha[x1 > x2] = x2
    return alpha.fillna(value=0)


def alpha78(volume, low, vwap):
    adv40 = op.sma(volume, 40)
    x1 = op.rank(op.correlation(op.ts_sum(((low * 0.352233) + (vwap * (1 - 0.352233))), 20), op.ts_sum(adv40, 20), 7))
    x2 = op.rank(op.correlation(op.rank(vwap), op.rank(volume), 6))
    alpha = x1.pow(x2)
    return alpha.fillna(value=0)


def alpha81(volume, vwap):
    adv10 = op.sma(volume, 10)
    x1 = op.rank(np.log(op.product(op.rank((op.rank(op.correlation(vwap, op.ts_sum(adv10, 50), 8)).pow(4))), 15)))
    x2 = op.rank(op.correlation(op.rank(vwap), op.rank(volume), 5))
    alpha = x1 < x2
    return alpha * -1


def alpha83(high, low, close, volume,vwap):
    x = op.rank(op.delay(((high - low) / (op.ts_sum(close, 5) / 5)), 2)) * op.rank(op.rank(volume))
    alpha = x / (((high - low) / (op.ts_sum(close, 5) / 5)) / (vwap - close))
    return alpha.fillna(value=0)


def alpha84(vwap, close):
    alpha = pow(op.ts_rank((vwap - op.ts_max(vwap, 15)), 21), op.delta(close, 5))
    return alpha.fillna(value=0)


def alpha85(volume, high, close, low):
    adv30 = op.sma(volume, 30)
    x1 = op.rank(op.correlation(((high * 0.876703) + (close * (1 - 0.876703))), adv30, 10))
    alpha = x1.pow(op.rank(op.correlation(op.ts_rank(((high + low) / 2), 4), op.ts_rank(volume, 10), 7)))
    return alpha.fillna(value=0)


def alpha86(volume, close, Open, vwap):
    adv20 = op.sma(volume, 20)
    x1 = op.ts_rank(op.correlation(close, op.sma(adv20, 15), 6), 20)
    x2 = op.rank(((Open + close) - (vwap + Open)))
    alpha = x1 < x2
    return alpha * -1


def alpha88(volume, Open, low, high, close):
    adv60 = op.sma(volume, 60)
    x1 = op.rank(op.decay_linear(((op.rank(Open) + op.rank(low)) - (op.rank(high) + op.rank(close))), 8))
    x2 = op.ts_rank(op.decay_linear(op.correlation(op.ts_rank(close, 8), op.ts_rank(adv60, 21), 8), 7), 3)
    alpha = x1
    alpha[x1 > x2] = x2
    return alpha.fillna(value=0)


def alpha92(volume, high, low, close, Open):
    adv30 = op.sma(volume, 30)
    x1 = op.ts_rank(op.decay_linear(((((high + low) / 2) + close) < (low + Open)), 15), 19)
    x2 = op.ts_rank(op.decay_linear(op.correlation(op.rank(low), op.rank(adv30), 8), 7), 7)
    alpha = x1
    alpha[x1 > x2] = x2
    return alpha.fillna(value=0)


def alpha94(volume, vwap):
    adv60 = op.sma(volume, 60)
    x = op.rank((vwap - op.ts_min(vwap, 12)))
    alpha = x.pow(op.ts_rank(op.correlation(op.ts_rank(vwap, 20), op.ts_rank(adv60, 4), 18), 3)) * -1
    return alpha.fillna(value=0)


def alpha95(volume, high, low, Open):
    adv40 = op.sma(volume, 40)
    x = op.ts_rank((op.rank(op.correlation(op.sma(((high + low) / 2), 19), op.sma(adv40, 19), 13)).pow(5)), 12)
    alpha = op.rank((Open - op.ts_min(Open, 12))) < x
    return alpha.fillna(value=0)


def alpha96(volume, vwap, close):
    adv60 = op.sma(volume, 60)
    x1 = op.ts_rank(op.decay_linear(op.correlation(op.rank(vwap), op.rank(volume), 4), 4), 8)
    x2 = op.ts_rank(op.decay_linear(op.ts_argmax(op.correlation(op.ts_rank(close, 7), op.ts_rank(adv60, 4), 4), 13), 14), 13)
    alpha = x1
    alpha[x1 < x2] = x2
    return alpha.fillna(value=0)


def alpha98(volume, Open, vwap):
    adv5 = op.sma(volume, 5)
    adv15 = op.sma(volume, 15)
    x1 = op.rank(op.decay_linear(op.correlation(vwap, op.sma(adv5, 26), 5), 7))
    alpha = x1 - op.rank(op.decay_linear(op.ts_rank(op.ts_argmin(op.correlation(op.rank(Open), op.rank(adv15), 21), 9), 7), 8))
    return alpha.fillna(value=0)


def alpha99(volume, high, low):
    adv60 = op.sma(volume, 60)
    x1 = op.rank(op.correlation(op.ts_sum(((high + low) / 2), 20), op.ts_sum(adv60, 20), 9))
    x2 = op.rank(op.correlation(low, volume, 6))
    alpha = x1 < x2
    return alpha * -1


def alpha101(close, Open, high, low):
    alpha = (close - Open) / ((high - low) + 0.001)
    return alpha


def BP(pb_lf):  # BP是市净率pb_lf的倒数，来自华泰研报
    # 定义一个函数，用于将一个数取倒数
    def reciprocal(x):
        if x == 0:
            return 0
        else:
            return 1 / x

    # 使用apply()函数将函数应用到每个单元格中
    BP = pb_lf.applymap(reciprocal)
    return BP


def EP(pe_ttm):  # EP是市盈率pe_ttm的倒数，来自华泰研报
    def reciprocal(x):
        if x == 0:
            return 0
        else:
            return 1 / x

    EP = pe_ttm.applymap(reciprocal)
    return EP


def SP(ps_ttm):  # SP是市销率ps_ttm的倒数，来自华泰研报
    def reciprocal(x):
        if x == 0:
            return 0
        else:
            return 1 / x

    SP = ps_ttm.applymap(reciprocal)
    return SP


def daoshu(dataf):
    return 0 if dataf == 0 else 1 / dataf


def std_60d(close):  # 个股最近 3个月内日收益率序列的标准差,华泰研报
    window = 60
    returns = close.pct_change()  # 计算收益率

    def stddev(df, window):  # 移动标准差
        return df.rolling(window).std()

    std_60d = -op.stddev(returns, window)
    return std_60d

def std_20d(close):  # 个股最近 20交易日内日收益率序列的标准差,华泰研报
    window = 20
    returns = close.pct_change()  # 计算收益率

    def stddev(df, window):  # 移动标准差
        return df.rolling(window).std()

    std_20d = -op.stddev(returns, window)
    return std_20d


def turnover14(turnover):
    turnover_14 = op.sma(turnover, 14)
    return turnover_14


def turnover28(turnover):
    turnover_28 = op.sma(turnover, 28)
    return turnover_28


def turnover14predicted(turnover_14, turnover_28):
    df_increase = (turnover_14 - turnover_28) / turnover_28
    return turnover_14 * (1 + df_increase)


def turnoveradvance01(turnover, pctchange, section_return, section_info, d=5, m=30, H=15):
    # d,m,H为参数，风险均值窗口d，收益加权窗口m，H一般为m的一半，作为半衰期
    # turnover为换手率的原始dataframe
    # pctchange为涨跌幅的原始dataframe
    # section_return为对应行业的涨跌幅的dataframe，行为行业指数，列为日期
    # section_info为股票及其对应的行业的对照表dataframe，列名为'industrycode'
    def weight_omega(m, j, H):
        aa = [2 ** (-i / H) for i in range(1, m + 1)]
        return 2 ** (-(m - j + 1) / H) / sum(aa)

    def risk_today(origin, d):
        return origin.rolling(d).mean() - origin

    weight_value = np.array([weight_omega(m, j, H) for j in range(1, m + 1)])

    stocklist = turnover.columns.intersection(section_info[section_info['industrycode'] != '0'].index)
    turnover = turnover[stocklist]
    pctchange = pctchange[stocklist]
    section_return = section_return.dropna(axis=1, how='any')
    search = section_info.applymap(lambda x: x in section_return.columns)
    selected = section_info[search.industrycode].index
    stocklist = turnover.columns.intersection(selected)
    turnover = turnover[stocklist]
    pctchange = pctchange[stocklist]

    df_exceed = pd.DataFrame(index=pctchange.index, columns=pctchange.columns)
    for ii in pctchange.columns:
        df_exceed[ii] = pctchange[ii] - section_return[section_info.loc[ii].values[0]]
    df_risk = pd.DataFrame(index=pctchange.index, columns=pctchange.columns)
    for ii in pctchange.columns:
        df_risk[ii] = risk_today(turnover[[ii]], d)
    df_riskturnover = df_risk * df_exceed
    df_riskturnover = df_riskturnover.iloc[d:, :]
    df_final = pd.DataFrame(index=df_riskturnover.index[m:], columns=df_riskturnover.columns)
    for jj in range(len(df_final.index)):
        df_final.iloc[jj, :] = weight_value @ df_riskturnover.iloc[jj:(jj + m), :].values
    return df_final


def AVT(dealnum, pctchange, section_return, section_info, volume, d=14, m=28, H=14):
    # d,m,H为参数，风险均值窗口d，收益加权窗口m，H一般为m的一半，作为半衰期
    # dealnum,volume为成交笔数、成交量的原始dataframe
    # pctchange为涨跌幅的原始dataframe
    # section_return为对应行业的涨跌幅的dataframe，行为行业指数，列为日期
    # section_info为股票及其对应的行业的对照表dataframe，列名为'industrycode'
    def weight_omega(m, j, H):
        aa = [2 ** (-i / H) for i in range(1, m + 1)]
        return 2 ** (-(m - j + 1) / H) / sum(aa)

    def risk_today(origin, d):
        return origin.rolling(d).mean() - origin

    weight_value = np.array([weight_omega(m, j, H) for j in range(1, m + 1)])

    stocklist = dealnum.columns.intersection(section_info[section_info['industrycode'] != '0'].index)
    dealnum = dealnum[stocklist]
    pctchange = pctchange[stocklist]
    volume = volume[stocklist]
    section_return = section_return.dropna(axis=1, how='any')
    search = section_info.applymap(lambda x: x in section_return.columns)
    selected = section_info[search.industrycode].index
    stocklist = dealnum.columns.intersection(selected)
    dealnum = dealnum[stocklist]
    pctchange = pctchange[stocklist]
    volume = volume[stocklist]

    df_exceed = pd.DataFrame(index=pctchange.index, columns=pctchange.columns)
    for ii in pctchange.columns:
        df_exceed[ii] = pctchange[ii] - section_return[section_info.loc[ii].values[0]]

    df_avt = volume / dealnum
    df_avt = df_avt ** (0.5)
    df_risk = pd.DataFrame(index=pctchange.index, columns=pctchange.columns)
    for ii in pctchange.columns:
        df_risk[ii] = risk_today(df_avt[[ii]], d)

    df_riskturnover = df_risk * df_exceed
    df_riskturnover = df_riskturnover.iloc[d:, :]
    df_final = pd.DataFrame(index=df_riskturnover.index[m:], columns=df_riskturnover.columns)
    for jj in range(len(df_final.index)):
        df_final.iloc[jj, :] = weight_value @ df_riskturnover.iloc[jj:(jj + m), :].values
    return df_final


def stdamount(amount, days=20):
    return -amount.rolling(30).std()


def sppercent(ps, days=242):
    return ps.applymap(daoshu).rolling(days).op.rank() / days


def bppercent(pb, days=242):
    return pb.applymap(daoshu).rolling(days).op.rank() / days

def IVR_FF3factor_1m (pb_lf,zz,returns,cap):
# 个股最近 N 个月内日收益率序列对 Fama-French 三因子（中证全指日收益率、总市值因子日收益率、BP 因子日收益率）进行多元线性回归的残差的标准差（N=1，3）

    #中证全指日收益率  1050*1
    zz_return = zz.pct_change()
    zz_return_df = pd.DataFrame(zz_return)

    # 计算因子收益率
    # 将 T 期因子值与 T+1 期个股收益率进行线性回归，得到的回归系数即为因子收益率。

    #BP因子日收益率 ,1050*1
    bp_returns = []
    bp = BP(pb_lf)
    for i in range(0, len(pb_lf)-1):
        X = bp.iloc[i, :].values.reshape(-1, 1)   # reshape(-1,1)是把X转换为列向量
        Y = returns.iloc[i + 1, :].values.reshape(-1, 1)
        X = sm.add_constant(X)  # 添加常数项
        model = sm.OLS(Y, X).fit()
        # 保存回归系数（去掉常数项）
        bp_returns.append(model.params[1]) # bp_returns是list
        # print(model.params[1])
    # 将回归系数转换为 DataFrame
    bp_returns_df = pd.DataFrame(bp_returns)


    #总市值因子日收益率 1050*1
    cap_returns = []
    for i in range(0, len(cap)-1):
        X1 = cap.iloc[i, :].values.reshape(-1, 1)
        Y = returns.iloc[i + 1, :].values.reshape(-1, 1)
        X1 = sm.add_constant(X1)  #添加常数项
        model = sm.OLS(Y, X1).fit()
        # 保存回归系数（去掉常数项）
        cap_returns.append(model.params[1])
    # 将回归系数转换为 DataFrame
    cap_returns_df = pd.DataFrame(cap_returns)


    # Fama-Franch多元线性回归，求残差的标准差

    #将因子收益率序列添加一个元素0，否则数据不能对齐无法回归
    x1 = zz_return_df.fillna(0)
    x2 = pd.concat([pd.DataFrame([0], columns=bp_returns_df.columns), bp_returns_df])
    x3 = pd.concat([pd.DataFrame([0], columns=cap_returns_df.columns), bp_returns_df])

    x1 = x1.reset_index(drop=True)  #对齐索引列
    x2 = x2.reset_index(drop=True)
    x3 = x3.reset_index(drop=True)

    X = pd.concat([x1, x2, x3], axis=1)
    X = X.iloc[1:, :]   # 去掉X的第一行0
    X.columns = ['中证全指', 'BP因子收益率', "总市值因子收益率"]
    Y = returns
    Y = Y.iloc[1:, :]   # 去掉Y的第一行
    window_size = 20   # 设置每个窗口的大小
    num_windows = Y.shape[0] - window_size + 1  # 计算窗口数量

    residuals_std_list = np.zeros((Y.shape[0], Y.shape[1]))
    # for j in range(window_size, len(X)):
    for j in range(1040, len(X)):
        print(j)
    # for j in range(window_size, 23):
        y = Y.iloc[j-window_size:j, :]  # 每次取最近一个windows的数据回归
        x = X.iloc[j-window_size:j, :]
        for k, col in enumerate(y.columns):
            y_col = y[col]  # y_col是个股收益率序列
            model = sm.OLS(y_col, sm.add_constant(x)).fit()
            residuals_std_col = model.resid.std()
            residuals_std_list[j, k] = residuals_std_col
            # print(residuals_std_list[j])

    residuals_std = pd.DataFrame(residuals_std_list, columns=y.columns)


    IVR_FF3factor_1m = residuals_std

    return IVR_FF3factor_1m


def IVR_CAPMfactor_3m(zz,returns,gz):
    # CAPM:个股最近 N 个月内（日收益率-无风险利率）序列对（中证全指日收益率-无风险利率）进行线性回归的残差的标准差
    # CAPM模型：ERi = rf + β(ERm - rf)
        # ERi - rf = β(ERm - rf)
        # Y = ERi - rf
        # X = (ERm - rf)
    # 相当于Y对X的无截距项回归，求其残差的标准差（波动率）
    # ERm:中证全指日收益率
    # ERi:个股日收益率
    # rf:无风险利率，用3M-SHIBOR-1年 代替
    # rf:无风险利率，用10年期国债到期收益率 代替
    # 中证全指日收益率
    zz_return = zz.pct_change()
    ERm = pd.DataFrame(zz_return)
    # 个股收益率
    ER = returns
    # 无风险利率
    rf = gz

    # 将因子收益率序列添加一个元素0，否则数据不能对齐无法回归
    ERm = ERm.fillna(0)
    ERm = ERm.reset_index(drop=True)  # 对齐索引列
    rf = rf.reset_index(drop=True)
    X = ERm.sub(rf.values.flatten(), axis=0)
    # X = X.iloc[1:, :]  # 去掉X的第一行0
    Y = ER.sub(rf.values.flatten(), axis=0)
    # Y = Y.iloc[1:, :]  # 去掉Y的第一行

    window_size = 60  # 设置每个窗口的大小
    num_windows = Y.shape[0] - window_size + 1  # 计算窗口数量

    residuals_std_list = np.zeros((Y.shape[0], Y.shape[1]))
    # for j in range(window_size, len(X)):
    for j in range(1050, len(X)):
        print(j)
        # for j in range(window_size, 23):
        y = Y.iloc[j - window_size:j, :]  # 每次取最近一个windows的数据回归
        x = X.iloc[j - window_size:j, :]
        for k, col in enumerate(y.columns):
            y_col = y[col]  # y_col是个股收益率序列
            model = sm.OLS(y_col, x).fit()  # 无截距项的回归
            residuals_std_col = model.resid.std()
            residuals_std_list[j, k] = residuals_std_col
            # print(residuals_std_list[j])
    residuals_std = pd.DataFrame(residuals_std_list, columns=y.columns)

    IVR_CAPMfactor_3m = residuals_std
    return IVR_CAPMfactor_3m

def Volume_Mean_20d_240d(volume):
    Volume_Mean_20d_240d = op.sma(volume,20)/op.sma(volume,240)
    return Volume_Mean_20d_240d




def bais(close):
    moving_average = op.sma(close,20)  # 计算最近n天的移动平均值
    bias = (close - moving_average) / moving_average * 100  # 计算乖离率
    return bias

def cci(high, low, close):
    typical_price = (high + low + close) / 3   # 计算典型价格
    typical_price.iloc[:9] = 0

    moving_average = op.sma(typical_price,10)  # 计算最近n天的典型价格移动平均值
    moving_average.iloc[:9] = 0

    mean_deviation = typical_price.rolling(window=10).mean().std()
    cci = (typical_price - moving_average) / (0.015 * mean_deviation)  # 计算CCI指标

    return cci

def ln_capital(cap):
    ln_capital = cap.applymap(np.log)
    return ln_capital


def Volume_CV_20d(volume):
    std = op.stddev(volume,20)
    mean = op.sma(volume,20)
    Volume_CV_20d = std/mean
    return Volume_CV_20d

def Volume_CV_60d(volume):
    std = op.stddev(volume,60)
    mean = op.sma(volume,60)
    Volume_CV_60d = std/mean
    return Volume_CV_60d