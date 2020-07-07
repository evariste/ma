
# https://math.stackexchange.com/questions/3745195/converting-recurrence-relation-to-linear-and-solve-with-matrix-exponentiation

import numpy as np

T = np.asarray(
    [[1, 0, 1, 1, 0, 0, 1, 0],
     [2, 0, 1, 0, 0, 0, 0, 1],
     [0, 1, 0, 0, 0, 0, 0, 0],
     [0, 0, 1, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 2, 0, 0, 0],
     [0, 0, 0, 0, 0, 4, 0, 0],
     [0, 0, 0, 0, 2, 0, 2, 0],
     [0, 0, 0, 0, 0, 4, 0, 4],
     ]
)

v = np.asarray([1, 1, 1, 1, 2, 4, 2, 4])


n_reps = 8


for k in range(n_reps):
    print(v)
    v = T.dot(v)

np.savetxt("T-latex-tab.txt", T, delimiter=' & ', fmt='%d', newline=' \\\\\n')
v0 = np.asarray([[1, 1, 1, 1, 2, 4, 2, 4]])
np.savetxt("v-latex-mat.txt", v0, delimiter=' & ', fmt='%d', newline=' \\\\\n')

print('done')
