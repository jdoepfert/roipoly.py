import pylab as pl
from roipoly import roipoly 

# create image
img = pl.ones((100, 100)) * range(0, 100)

# show the image
pl.imshow(img, interpolation='nearest', cmap="Greys")
pl.colorbar()
pl.title("left click: line segment         right click: close region")

# let user draw first ROI
ROI1 = roipoly(roicolor='r') #let user draw first ROI

# show the image with the first ROI
pl.imshow(img, interpolation='nearest', cmap="Greys")
pl.colorbar()
ROI1.displayROI()
pl.title('draw second ROI')

# let user draw second ROI
ROI2 = roipoly(roicolor='b') #let user draw ROI

# show the image with both ROIs and their mean values
pl.imshow(img, interpolation='nearest', cmap="Greys")
pl.colorbar()
[x.displayROI() for x in [ROI1, ROI2]]
[x.displayMean(img) for x in [ROI1, ROI2]]
pl.title('The two ROIs')
pl.show()

# show ROI masks
pl.imshow(ROI1.getMask(img) + ROI2.getMask(img),
          interpolation='nearest', cmap="Greys")
pl.title('ROI masks of the two ROIs')
pl.show()


