import pandas as pd
from plot import plot
import matplotlib.pyplot as plt


path="C:\\Users\\gishy\\OneDrive - University of Bath\\Bath Thesis\\Bath Thesis\\results\\csvs\\efficientdet_b1_results.csv"

df=pd.read_csv(path)


iou_05_indexes=[1,15,23,31,39,47]
iou_095_indexes=[2,16,24,32,40,48]
train_total_losses=[5,19,27,35,43,51]


names=["No Augmentation","Blending Sequence","Blurring Sequence","Geometric Sequence","(3x4) Grid Sequence","(3x5) Grid Sequence with Transfer Learning"]

if __name__=="__main__":



	# for i in iou_05_indexes:
	# 	print(max(df.iloc[:,i]))
		
	for index,name in enumerate(df.columns):
		print(index,name)

	
	plot(df,iou_05_indexes,names,title="mAP 0.5: EfficientDet",rolling_mean_windows_size=5,xlabel="Epochs",ylabel="Percentage",number_of_rows=80,percentage=True,legend_outside=False)
	plot(df,iou_095_indexes,names,title="mAP 0.5:0.95: EfficientDet",rolling_mean_windows_size=5,xlabel="Epochs",ylabel="Percentage",number_of_rows=80,percentage=True,legend_outside=False)
	plot(df,train_total_losses,names,title="Total Training Loss: EfficientDet",rolling_mean_windows_size=5,xlabel="Epochs",ylabel="Value",number_of_rows=80,legend_outside=False)
	
	