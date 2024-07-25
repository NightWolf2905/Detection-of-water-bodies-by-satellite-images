# -*- coding: utf-8 -*-
"""Detection of water bodies from  satellite images.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1I1bOmW_YS3z0-mnkCYNZHxozd_JwOJ1e
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install rasterio

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import rasterio as rio

ds = rio.open(r"/content/drive/MyDrive/archive_2/y_train.tif")

arr = ds.read()
arr = np.where(np.isnan(arr),0,arr)
arr = np.moveaxis(arr,0,-1)
arr.shape

y_train = np.reshape(arr, (arr.shape[0] * arr.shape[1],arr.shape[2]))
y_train.shape

ds = rio.open(r"/content/drive/MyDrive/archive_2/X_train.tif")

arr = ds.read()
arr = np.where(np.isnan(arr),0,arr)
arr = np.moveaxis(arr,0,-1)
arr.shape

x_train = np.reshape(arr, (arr.shape[0] * arr.shape[1],arr.shape[2]))
x_train.shape

nrow_train = arr[0]
ncol_train = arr[1]
ds.close()

ds = rio.open(r"/content/drive/MyDrive/archive_2/X_test.tif")
arr = ds.read()
arr = np.where(np.isnan(arr),0,arr)
arr = np.moveaxis(arr,0,-1)
arr.shape
x_test = np.reshape(arr, (arr.shape[0] * arr.shape[1],arr.shape[2]))
print(x_test.shape)
nrow_test = arr[0]
ncol_test = arr[1]
ds.close()

ds = rio.open(r"/content/drive/MyDrive/archive_2/y_test.tif")
arr = ds.read()
arr = np.where(np.isnan(arr),0,arr)
arr = np.moveaxis(arr,0,-1)
arr.shape
y_test = np.reshape(arr, (arr.shape[0] * arr.shape[1],arr.shape[2]))
print(y_test.shape)
nrow_test = arr.shape[0]
ncol_test = arr.shape[1]
ds.close()

from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier(n_estimators = 100, random_state = 42, verbose = 3, n_jobs = -1)
rfc.fit(x_train,y_train)

y_pred = rfc.predict(x_test)

from sklearn.metrics import classification_report
print(classification_report(y_test,y_pred))

y_pred.shape

y_pred_reshaped = y_pred.reshape(nrow_test,ncol_test)
y_test_reshaped = y_test.reshape(nrow_test,ncol_test)
x_test_reshaped = x_test.reshape(nrow_test,ncol_test,4)
print(y_pred_reshaped.shape, x_test_reshaped.shape)

fig, axes = plt.subplots(nrows =1, ncols =4,sharex = True, sharey = True, figsize =(15,7))
ax1,ax2,ax3,ax4 = axes.flatten()

ax1.set_title("RGB",fontweight = 'bold', fontsize = '16')
ax1.imshow(x_test_reshaped[:,:,:3])

ax2.set_title("NRI", fontweight= 'bold', fontsize = '16')
ax2.imshow(x_test_reshaped[:,:,-1])

ax3.set_title("Ground Truth", fontweight= 'bold', fontsize = '16')
ax3.imshow(y_test_reshaped[:,:])

ax4.set_title("Predicted", fontweight= 'bold', fontsize = '16')
ax4.imshow(y_pred_reshaped[:,:,])
plt.show()