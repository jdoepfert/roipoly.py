import logging

import numpy as np
from matplotlib import pyplot as plt

from roipoly import MultiRoi

logging.basicConfig(format='%(levelname)s ''%(processName)-10s : %(asctime)s '
                           '%(module)s.%(funcName)s:%(lineno)s %(message)s',
                    level=logging.INFO)

# Create image
img = np.ones((100, 100)) * range(0, 100)

# Show the image
fig = plt.figure()
plt.imshow(img, interpolation='nearest', cmap="Greys")
plt.colorbar()

# Add multiple ROIs
plt.title("Click on the button to add a new ROI")
multiroi = MultiRoi(fig=fig)

# Draw all ROIs
plt.imshow(img, interpolation='nearest', cmap="Greys")
for roi in multiroi.rois:
    roi.display_roi()
    roi.display_mean(img)
plt.show()
