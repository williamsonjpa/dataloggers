import os
import glob
import pandas as pd

def merge(root):
    indir = root + '/Data/Appended/'
    os.chdir(indir)
    fileList=glob.glob('*csv')
    dfList=[]
    colnames=pd.read_csv(fileList[0]).columns
    for filename in fileList:
        df=pd.read_csv(filename)
        df = df.drop("Unnamed: 0", axis=1)
        dfList.append(df)
    concatDf=pd.concat(dfList,axis=0)#this concatenates vertically (axis=0)
    concatDf.columns=colnames[1:]
    concatDf.to_csv(root + '/Data/Final/merge.csv',index=None)



   