import pandas as pd
from plot import plot
import numpy as np


path="C:\\Users\\gishy\\OneDrive - University of Bath\\Bath Thesis\\Bath Thesis\\results\\csvs\\retinanet_results.csv"
df=pd.read_csv(path)


map_05_indices=[0,5,10,15,20,25]
map0_05_095_indices=[1,6,11,16,21,26]
train_running_loss=[4,7,14,19,22,29]


names=["No Augmentation","Blending Sequence","Blurring Sequence","Geometric Sequence","(3x4) Grid Augmentation","(3x5) Grid Augmentation"]


if __name__=="__main__":

	# for i in map_05_indices:
	# 	print(max(df.iloc[:20,i]))

	# for index,name in enumerate(df.columns):
	# 	print(index,name)

	for index,(i,j) in enumerate(zip(map_05_indices,map0_05_095_indices)):
		
		maximum=max(df.iloc[:20,i])
		print(index,names[index],maximum,max(df.iloc[:20,j]))

	# print(np.std(df.iloc[:20,5]))
	# print(np.std(df.iloc[:20,4]))
	# print(np.std(df.iloc[:20,3]))
	# print(np.std(df.iloc[:20,0]))




	plot(df,map_05_indices,names,title="mAP 0.5: RetinaNet",number_of_rows=20,rolling_mean_windows_size=3,xlabel="Epochs",ylabel="Percentage",percentage=True,legend_outside=True)
	plot(df,map0_05_095_indices,names,title="mAP 0.5:0.95: RetinaNet",number_of_rows=20,rolling_mean_windows_size=3,xlabel="Epochs",ylabel="Percentage",percentage=True,legend_outside=True)
	plot(df,train_running_loss,names,title="Running Training Loss: RetinaNet",number_of_rows=20,rolling_mean_windows_size=3,xlabel="Epochs",ylabel="Value",legend_outside=True)
 