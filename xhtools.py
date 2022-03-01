import pandas as pd
import numpy as np

class Xhtools:
    '''
    npproduct:求两个一维数组的笛卡尔积
    threesigmod:根据3Sigma法则求异常值
    numericoutlier:箱线图法求异常值
    cutbin:自定义分箱，woe、iv值计算
    '''
    def __init__(self):
        return None
    
    def npproduct(self,array1,array2):
        if len(array1) == len(array2):
            return np.transpose([np.repeat(array1, len(array1)), np.tile(array2, len(array2))])
        else:
            return 'array1、array2长度需一致'
        
    def threesigmod(self,array1,array2):
        avg = np.mean(array1)
        std = np.std(array1)
        threshold_up = float(avg + 3*std)
        threshold_down = float(avg -3*std)
        errornum = list(filter(lambda s:(s< threshold_down)|(s> threshold_up),array2))
        return errornum
    
    def numericoutlier(self,array1,array2):
        iqr = np.quantile(array1,0.75) - np.quantile(array1,0.25)
        q_down = float(np.quantile(array1,0.25)-1.5*iqr)
        q_up = float(np.quantile(array1,0.75)+1.5*iqr)
        errornum = list(filter(lambda s:(s<q_down)|(s>q_up),array2))
        return errornum
    
    def cutbin(self,x,y,cut): # x为待分箱的变量，y为target变量,cut为自定义的分箱(list)
        total = y.count()  # 计算总样本数
        bad = y.sum()      # 计算坏样本数
        good = y.count()-y.sum()  # 计算好样本数
        d1 = pd.DataFrame({'x':x,'y':y,'bucket':pd.cut(x,cut)}) 
        d2 = d1.groupby('bucket',as_index=True)  # 按照分箱结果进行分组聚合
        d3 = pd.DataFrame(d2.x.min(),columns=['min_bin']) 
        d3['min_bin'] = d2.x.min()  # 箱体的左边界
        d3['max_bin'] = d2.x.max()  # 箱体的右边界
        d3['bad'] = d2.y.sum()  # 每个箱体中坏样本的数量
        d3['total'] = d2.y.count() # 每个箱体的总样本数
        d3['bad_rate'] = d3['bad']/d3['total']  # 每个箱体中坏样本所占总样本数的比例
        d3['badattr'] = d3['bad']/bad   # 每个箱体中坏样本所占坏样本总数的比例
        d3['goodattr'] = (d3['total'] - d3['bad'])/good  # 每个箱体中好样本所占好样本总数的比例
        d3['woe'] = np.log(d3['goodattr']/d3['badattr'])  # 计算每个箱体的woe值
        iv = ((d3['goodattr']-d3['badattr'])*d3['woe']).sum()  # 计算变量的iv值
        d4 = (d3.sort_values(by='min_bin')).reset_index(drop=True) # 对箱体从大到小进行排序
        woe = list(d4['woe'].round(3))
        return d4,iv,woe