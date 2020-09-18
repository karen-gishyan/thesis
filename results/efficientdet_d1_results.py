import pandas as pd
from plot import plot
import matplotlib.pyplot as plt
import numpy as np


path="C:\\Users\\gishy\\OneDrive - University of Bath\\Bath Thesis\\Bath Thesis\\results\\csvs\\efficientdet_b1_results.csv"

df=pd.read_csv(path)

print("Go on")
iou_05_indexes=[1,15,23,31,39,47]
iou_095_indexes=[2,16,24,32,40,48]
train_total_losses=[5,19,27,35,43,51]


names=["No Augmentation","Blending Sequence","Blurring Sequence","Geometric Sequence","(3x4) Grid Augmentation","(3x5) Grid Augmentation with Transfer Learning"]



if __name__=="__main__":

	for index,name in enumerate(df.columns):
		print(index,name)


	for index,(i,j) in enumerate(zip(iou_05_indexes,iou_095_indexes)):
		
		maximum=max(df.iloc[:25,i])
		print(index,names[index],maximum,max(df.iloc[:25,j]))

	
	plot(df,iou_05_indexes,names,title="mAP 0.5: EfficientDet-D1",rolling_mean_windows_size=3,xlabel="Epochs",ylabel="Percentage",number_of_rows=25,percentage=True,legend_outside=True)
	plot(df,iou_095_indexes,names,title="mAP 0.5:0.95: EfficientDet-D1",rolling_mean_windows_size=3,xlabel="Epochs",ylabel="Percentage",number_of_rows=25,percentage=True)
	plot(df,train_total_losses,names,title="Total Training Loss: EfficientDet-D1",rolling_mean_windows_size=3,xlabel="Epochs",ylabel="Value",number_of_rows=25)
	
	