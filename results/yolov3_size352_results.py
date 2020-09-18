import pandas as pd
from plot import plot
import sys

path="C:\\Users\\gishy\\OneDrive - University of Bath\\Bath Thesis\\Bath Thesis\\results\\csvs\\yolov3_result_352s.csv"
df=pd.read_csv(path)



map_05_indices=[10,25,40,55,70,85]
f1_indices=[11,26,41,56,71,86]
total_loss=[5,20,35,50,65,80]


names=["No Augmentation","Blending Sequence","Blurring Sequence","Geometric Sequence","(3x4) Grid Augmentation","(3x5) Grid Augmentation with Transfer Learning"]


if __name__=="__main__":


	for index,name in enumerate(df.columns):
		print(index,name)

	for index,(i,j) in enumerate(zip(map_05_indices,f1_indices)):
		
		maximum=max(df.iloc[:15,i])
		print(index,names[index],maximum,max(df.iloc[:15,j]))


	plot(df,map_05_indices,names,title="mAP 0.5: Yolov 3-SPP (352,352) size",rolling_mean_windows_size=3,xlabel="Epochs",ylabel="Percentage",number_of_rows=15,percentage=True)		
	plot(df,f1_indices,names,title="F1 score: Yolov 3-SPP (352,352) size",rolling_mean_windows_size=3,xlabel="Epochs",ylabel="Percentage",number_of_rows=15,percentage=True)
	plot(df,total_loss,names,title="Total Training Loss:Yolov 3-SPP (352,352) size",rolling_mean_windows_size=3,xlabel="Epochs",number_of_rows=15,ylabel="Value")
	
