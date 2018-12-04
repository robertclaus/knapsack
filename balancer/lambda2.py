import numpy as np

def handler(event):
    try:
    	# n = event[0]
    	n = 5000
        matrix_inversion(n)
        # applyPredefinedProfile(interval_len, usage_lvl)
    except Exception as e:
return {'error': str(e)} 


def matrix_inversion(n):
    A = np.random.rand(n,n)
    pos_def_mat = np.dot(A, A.transpose())
    np.linalg.inv(pos_def_mat)