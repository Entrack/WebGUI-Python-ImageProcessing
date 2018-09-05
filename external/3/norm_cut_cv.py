from skimage import data, segmentation, color
from skimage.future import graph
from matplotlib import pyplot as plt

import os
# filename = '/home/jonathan/Coding/Python/FIT_ImageProcessing/backend/resources/images/lenna.png'
filename = '64.gif'
from skimage import io
img = io.imread(filename)

# img = data.coffee()

labels1 = segmentation.slic(img, compactness=10, n_segments=12)
out1 = color.label2rgb(labels1, img, kind='avg')

g = graph.rag_mean_color(img, labels1, mode='similarity')
labels2 = graph.cut_normalized(labels1, g)
out2 = color.label2rgb(labels2, img, kind='avg')

fig, ax = plt.subplots(nrows=2, sharex=True, sharey=True, figsize=(6, 8))

ax[0].imshow(out1)
ax[1].imshow(out2)

for a in ax:
    a.axis('off')

plt.tight_layout()
plt.show()