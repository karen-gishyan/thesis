import pandas as pd
import matplotlib.pyplot as plt
import sys

path="C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\efficientdet final results.csv"


efficient=pd.read_csv(path)


# for index,name in enumerate(efficient.columns):
# 	print(index,name)


iou_05_indexes=[1,15,23,31]
iou_095_indexes=[2,16,24,32]
train_losses=[5,11,19,27,35]
classifcation_losses=[3,9,17,25,33]

for i in iou_05_indexes:

	plt.plot(efficient.iloc[:50,i]*100,label=efficient.columns[i])
	
	
l=plt.legend()
names=["No Augmentation","Blending Augmentation","Blurring Augmentation","Geometric Augmentation"]
[l.get_texts()[i].set_text(j) for i,j in zip(range(len(l.get_texts())),names)]

plt.title("AP:0.5 Efficientdet Results")
plt.xlabel("Epochs")
plt.ylabel("AP %")
plt.show()
plt.clf()

for i in iou_095_indexes:

	plt.plot(efficient.iloc[:50,i]*100,label=efficient.columns[i])


l=plt.legend()

names=["No Augmentation","Blending Augmentation","Blurring Augmentation","Geometric Augmentation"]

[l.get_texts()[i].set_text(j) for i,j in zip(range(len(l.get_texts())),names)]

plt.title("AP:0.95 Efficientdet Results")
plt.xlabel("Epochs")
plt.ylabel("AP %")
plt.show()
plt.clf()



for i in train_losses:

	plt.plot(efficient.iloc[:50,i]*100,label=efficient.columns[i])


l=plt.legend()

names=["No Augmentation","Transfer Learning with no Augmentation","Blending Augmentation","Blurring Augmentation","Geometric Augmentation"]

[l.get_texts()[i].set_text(j) for i,j in zip(range(len(l.get_texts())),names)]

plt.title("Efficientdet Training Total  Loss")
plt.xlabel("Epochs")
plt.ylabel("Total Loos Number")
plt.show()
plt.clf()



for i in classifcation_losses:

	plt.plot(efficient.iloc[:50,i]*100,label=efficient.columns[i])


l=plt.legend()

names=["No Augmentation","Trasnfer Learning with no Augmentation","Blending Augmentation","Blurring Augmentation","Geometric Augmentation"]

[l.get_texts()[i].set_text(j) for i,j in zip(range(len(l.get_texts())),names)]

plt.title("Efficientdet Training Classification Loss")
plt.xlabel("Epochs")
plt.ylabel("Total Loos Number")
plt.show()
plt.clf()
