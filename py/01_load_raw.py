import os
import numpy as np

# Set filename
filename = os.path.join(os.getcwd(), '..', 'data', 'workspace', '001', 'lh_thick_2e-4.raw')

# Load filename
data = np.fromfile(filename)
