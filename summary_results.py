import pandas as pd 
import matplotlib.pyplot as plt 
import os
import seaborn as sns
import sys


names=["EfficientDet-D1","EfficientDet-D4","RetinaNet","Yolov3-SPP-352","Yolov3-SPP-1056","Yolov5-Large-352","Yolov5-Large-1056"]
values=[5.4,16.4,22.3,18.8,48.6,11.1,36.5]

names_sorted=[y for  _,y in  sorted(zip(values,names),key=lambda pair: pair[0])]
values_sorted=sorted(values)


data=pd.DataFrame({"Models":names_sorted,"Values":values_sorted})


ax=data.plot(x="Models",kind="bar",rot=0)
ax.legend(["mAP 0.5"])
ax.set_title("Models ordered by their best performance")
ax.set_ylabel("Percentage")


for i in ax.patches:
    
    ax.text(i.get_x(), i.get_height()+.5, str((i.get_height()))+'%')# fontsize=15, color='dimgrey')

plt.show()



