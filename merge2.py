import os
import glob
import pandas as pd

def merge(root):
    os.chdir(root + '/Data/Appended/')
    fileList=glob.glob('*csv')
    dfList=[]
    colnames=pd.read_csv(fileList[0]).columns[2:]
    print(colnames)
    for filename in fileList:
        df=pd.read_csv(filename)
        df = df[colnames]
        dfList.append(df)
    concatDf=pd.concat(dfList,axis=0)#this concatenates vertically (axis=0)
    concatDf.columns=colnames
    concatDf.to_csv(root + '/Data/Final/merge.csv',index=None)
