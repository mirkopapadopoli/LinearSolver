import os
import csv
import time
import numpy as np

import scipy.io
import scipy.sparse
from scipy.io import mmread
from scipy.linalg import norm
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve

from sksparse.cholmod import cholesky

def sparse_solve(A,b):

    chol = True
    start = time.perf_counter()
    try:
        x = cholesky(A)(b)
        
    except Exception as e:
        chol = False
        x = spsolve(A, b)   

    finally:
        stop = time.perf_counter()
        fntime = stop - start
        erel = norm(x - xe) / norm(xe)

    return [chol, fntime, erel]




A = mmread("/Users/mirkopapadopoli/Desktop/Unimib/Metodi del Calcolo Scientifico/Progetto1/Matrix/ex15.mtx")
A = csc_matrix(A)
nnz = A.count_nonzero()
            
# Create array [1...1]
size = A.shape[0]        
xe = np.ones(size)

# Create b
b = A*xe
#print('Run ' + filename + ' ...')

# Solve
[chol, tot_time, erel] = sparse_solve(A,b)

# process = psutil.Process(os.getpid())    
# with open('../reports/python_linux.csv', 'w+', newline='') as file:
#     writer = csv.writer(file)
#     # Set csv header 
#     writer.writerow(["Matrix", "NNZ", "Time", "Memory", "RelError", "isCholesky"])
    
#     for filename in os.listdir('../matrixes/'):
        
#         if filename.endswith(".mtx"):
#             print('Import ' + filename + ' ...')

#             # Read the matrix
#             A = mmread('../matrixes/' + filename)
#             A = csc_matrix(A)
#             nnz = A.count_nonzero()
            
#             # Create array [1...1]
#             size = A.shape[0]        
#             xe = np.ones(size)

#             # Create b
#             b = A*xe
#             print('Run ' + filename + ' ...')

#             # Solve
#             [chol, tot_time, erel] = sparse_solve(A,b)
            
#             #convert from byte to MB
#             mem_usage = process.memory_info().rss / 10**6
#             writer.writerow([filename, nnz, tot_time, mem_usage, erel, chol])
            

