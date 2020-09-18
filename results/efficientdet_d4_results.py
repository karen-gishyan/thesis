import pandas as pd
from plot import plot
import matplotlib.pyplot as plt


path="C:\\Users\\gishy\\OneDrive - University of Bath\\Bath Thesis\\Bath Thesis\\results\\csvs\\efficientdet_b4_results.csv"

df=pd.read_csv(path)


iou_05_indexes=[1,9,17,25,33,41]
iou_095_indexes=[2,10,18,26,34,42]
train_total_losses=[5,13,21,29,37,45]


names=["No Augmentation","Blending Sequence","Blurring Sequence","Geometric Sequence","(3x4) Grid Augmentation","(3x5) Grid Augmentation with Transfer Learning"]

if __name__=="__main__":

	
	for index,name in enumerate(df.columns):
		print(index,name)

	for index,(i,j) in enumerate(zip(iou_05_indexes,iou_095_indexes)):
		
		maximum=max(df.iloc[:15,i])
		print(index,names[index],maximum,max(df.iloc[:15,j]))

		
	plot(df,iou_05_indexes,names,title="mAP 0.5: EfficientDet-D4",rolling_mean_windows_size=3,xlabel="Epochs",ylabel="Percentage",percentage=True,legend_outside=True)
	plot(df,iou_095_indexes,names,title="mAP 0.5:0.95: EfficientDet-D4",rolling_mean_windows_size=3,xlabel="Epochs",ylabel="Percentage",percentage=True,legend_outside=True)
	plot(df,train_total_losses,names,title="Total Training Loss: EfficientDet-D4",rolling_mean_windows_size=3,xlabel="Epochs",ylabel="Value",legend_outside=True)
	
	 