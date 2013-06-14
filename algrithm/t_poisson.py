import numpy as np
Expect = 100
Size = 1000
s = np.random.poisson(Expect, Size)

# Display histogram of the sample:

import matplotlib.pyplot as plt
count, bins, ignored = plt.hist(s, normed=True)
plt.xlabel('s')
plt.ylabel('Prob')
plt.show()
