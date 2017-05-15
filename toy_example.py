import sys
import skimage.io
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import dask
import dask.array as da
import numpy as np
from dask.dot import dot_graph
from dask.distributed import Client, LocalCluster
from dask.distributed import Scheduler
from skimage.filters import threshold_otsu
from skimage.feature import blob_dog, blob_log, blob_doh
from skimage import data, segmentation, color, filters, io
from skimage.future import graph 

sample = skimage.io.imread('/Users/nivethamahalakshmibalasamy/Documents/ECI-PolarScience/dask_stuff/grayscale-xy-1376.png')
im = data.camera()
# #skimage.io.imshow(sample)
# plt.imshow(sample)
# plt.show()

# Loop through set of images and display them

def sample_images():
	samples = [skimage.io.imread('/Users/nivethamahalakshmibalasamy/Documents/ECI-PolarScience/dask_stuff/grayscale-xy-%d.png' %i) for i in [1376,1377,1378,1379,1380,1381,1382,1383,1384]]

	fig, axarr = plt.subplots(1, 9, sharex=True, sharey=True, figsize=(24, 2.5))
	print axarr
	for i, sample in enumerate(samples):
		axarr[i].imshow(sample)
	plt.show()


# Read images using delayed function into an image array
def array_images():
	custom_imread = dask.delayed(skimage.io.imread, pure = True)
	images = [custom_imread('/Users/nivethamahalakshmibalasamy/Documents/ECI-PolarScience/dask_stuff/grayscale-xy-%d.png' %i) for i in range(1376, 1396)]
	#print images
	image_array = [da.from_delayed(i, sample.shape, sample.dtype) for i in images]
	sizes =  [j.shape for j in image_array]
	#print sizes
	stack = da.stack(image_array, axis = 0)
	print stack
	#print stack[0]
	# Combining chunks - A chunk consists of 5 images
	stack = stack.rechunk((5, 2000, 2000))
	print "After rechunking: "
	temp = stack
	#temp.visualize()
	print "Before distributing to workers:"
	print stack.mean().compute()
	print stack[1, :].compute()
	print stack[19, :].mean().compute()
	stack.visualize()

	# Distribute array components over workers and centralized scheduler
	cluster = LocalCluster()
	client = Client(cluster)
	print client

	# Load the entire distributed array on the cluster (4 workers, 4 cores)
	stack = client.persist(stack)
	#print stack.shape
	#print "After distributing to workers: "
	print stack.mean().compute()

	# map the otsu thresholding function
	#print stack[0]
	stack = da.map_blocks(otsu_thresholding, stack, chunks = (5,2000,2000), dtype = sample.dtype)
	stack = da.map_blocks(blob_detection, stack, chunks = (5,2000,2000), dtype = sample.dtype)
	stack = client.persist(stack)
	#th = client.persist(th)
	#thresholded.visualize()
	#th = client.persist(thresholded)
	#print thresholded.mean().compute()
	#print thresholded
	#print stack.shape
	print stack.mean().compute()
	stack.visualize()
	#th.visualize()


def otsu_thresholding(image):
	thresh = threshold_otsu(image)
	print image.shape
	binary = image > thresh
	# fig, axes = plt.subplots(ncols=3, figsize=(8, 2.5))
	# ax = axes.ravel()

	# ax[0] = plt.subplot(1, 3, 1, adjustable='box-forced')
	# ax[1] = plt.subplot(1, 3, 2)
	# ax[2] = plt.subplot(1, 3, 3, sharex=ax[0], sharey=ax[0], adjustable='box-forced')

	# ax[0].imshow(image, cmap=plt.cm.gray)
	# ax[1].hist(image.ravel(), bins=256)
	# ax[2].imshow(binary, cmap=plt.cm.gray)

	# plt.show()
	return binary


def otsu():
	threshold = threshold_otsu(im)
	bin = im > threshold
	print bin


def segmentation(image):
	label = segmentation.slic(image, compactness = 30, n_segments = 40)


def blob_detection(image):
	blobs_doh = blob_doh(image, max_sigma=30, threshold=.01)
	print blob_doh	
	




if __name__ == '__main__':
	#sample_images()
	array_images()
	#otsu_thresholding(sample)
	#otsu()






