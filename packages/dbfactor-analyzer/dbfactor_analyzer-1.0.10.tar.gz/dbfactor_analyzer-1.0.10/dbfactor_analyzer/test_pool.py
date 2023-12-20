#%%
import dbfactor_analyzer.analyze as db
import dbfactor_analyzer.factor as df
import dbfactor_analyzer.prepare as dp
#%%
from multiprocessing import  Process

def fun1(name):
    print('测试%s多进程' %name)

if __name__ == '__main__':
    process_list = []
    for i in range(5):  #开启5个子进程执行fun1函数
        p = Process(target=fun1,args=('Python',)) #实例化进程对象
        p.start()
        process_list.append(p)

    for i in process_list:
        p.join()

    print('结束测试')
# %%
demeaned=True
group_adjust=True
by_group=False
turnover_periods=14
avgretplot=(5,15)
std_bar=False

import pandas as pd 
import numpy as np

close = pd.read_csv(r"C:\Users\14681\Desktop\factor_test\make_alpha\base_data\close_hfq.csv", index_col=0).fillna(value=0)
pb_lf = pd.read_csv(r'C:\Users\14681\Desktop\factor_test\make_alpha\base_data\pb_lf.csv',  index_col=0)

industry_df=pd.read_csv(r'C:\Users\14681\Desktop\factor_test\test_factor\industry申万三级.csv' , encoding='gbk')
BP=df.BP(pb_lf)
BP.index=close.index
BP_slice=BP.loc['2022/1/4':,:]
groupby=dp.industry_info_todict(industry_df)
fac_BP_all=db.FactorAnalyzer(BP_slice,close,groupby=groupby,weights=1.0,quantiles=5,bins=None,periods=(14,),binning_by_group=False)
# %%
from multiprocessing import Process
if __name__=='__main__':
    p1=Process(target=fac_BP_all.plot_quantile_statistics_table,args=(demeaned,group_adjust,))
    p2=Process(target=fac_BP_all.plot_returns_table(demeaned,group_adjust,))
    p3=Process(target=fac_BP_all.plot_quantile_returns_bar,args=(by_group,demeaned,group_adjust,))
    p4=Process(target=fac_BP_all.plot_cumulative_returns_by_quantile,args=(turnover_periods,demeaned,group_adjust,))
    p5=Process(target=fac_BP_all.plot_cumulative_returns_by_quantile_last,args=(demeaned,group_adjust,))
    p6=Process(target=fac_BP_all.plot_cumulative_returns,args=(turnover_periods,demeaned,group_adjust,))
    p7=Process(target=fac_BP_all.plot_top_down_cumulative_returns,args=(turnover_periods,demeaned,group_adjust,))
    p8=Process(target=fac_BP_all.plot_mean_quantile_returns_spread_time_series,args=(demeaned,group_adjust,))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p7.start()
    p8.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()
    p7.join()
    p8.join()


# %%
