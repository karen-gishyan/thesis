import pandas as pd
from plot import plot


path="C:\\Users\\gishy\\OneDrive - University of Bath\\Bath Thesis\\Bath Thesis\\results\\final csvs\\retinanet final results.csv"
df=pd.read_csv(path)


map_05_indices=[0,5,10,15,20]
map0_05_095_indices=[1,6,11,16,21]
train_cls_loss=[2,7,12,17,22]
train_regression_loss=[3,8,13,18,23]
train_running_loss=[4,9,14,19,24]


for i in map_05_indices:
	print(max(df.iloc[:,i]))



#names=["No Augmentation","Blending Augmentation","Blurring Augmentation","Geometric Augmentation"]
names=["No Augmentation","Blending Augmentation","Blurring Augmentation","Geometric Augmentation","(3,4)-Gridlike Augmentation"]


if __name__=="__main__":

	for index,name in enumerate(df.columns):
		print(index,name)
	#plot(df,map_05_indices,names,title="MaP 0.5 results: Retinanet",xlabel="Epochs",ylabel="AP/MAP")
	#plot(df,map0_05_095_indices,names,title="MaP 0.5:0.95 results: Retinanet",xlabel="Epochs",ylabel="AP/MaP")
	plot(df,train_cls_loss,names,title="Train Classification Loss: Retinanet",xlabel="Epochs",ylabel="Value")
	#plot(df,train_regression_loss,names,title="Train Regression Loss: Retinanet",xlabel="Epochs",ylabel="Value")
	#plot(df,train_running_loss,names,title="Train Running Loss",xlabel="Epochs",ylabel="Value")