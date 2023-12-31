import numpy as np
import scipy.linalg as sc
import os, csv, platform, psutil

from scipy.sparse.linalg import spsolve
from scipy.sparse import csc_matrix
from scipy.io import mmread
from datetime import datetime
from memory_profiler import memory_usage

path_data = "C:/Users/papad/Code/LinearSolver/Data/"
path_matrix = "C:/Users/papad/Code/LinearSolver/Matrix MTX/"
header_csv = [
    "Software",
    "Sistema",
    "Matrice",
    "Dimensione",
    "Errore Relativo",
    "Tempo Esecuzione (sec)",
    "Memoria (MB)",
]


def calculateFunction(matrixList):
    # Read Matrix and convert to Compressed Sparse Row matrix
    M = mmread(path_matrix + matrixList)  # .tocsc()
    M = csc_matrix(M)
    # Print Matrix Name and Dimension
    # print("Matrix: ", matrixList)
    dimension = M.shape
    # print("Dimension: ", M.shape)

    # Identify the matrix
    xe = np.ones(M.shape[0])

    # Creo il vettore b
    b = M * xe
    print("Eseguo " + matrixList + " ...")
    # Start timer
    # startTime = time.process_time()
    startTime = datetime.now()
    # print(startTime)
    # Start Memory
    startMemory = psutil.swap_memory()[1] / (1024**2)

    # Decomposition Cholesky
    # M = sc.cholesky(M.todense(), lower=True)

    # Calculate the solution of the linear system
    x = spsolve(M, b)  # , use_umfpack=True)

    # End Memory
    endMemory = max(memory_usage((spsolve, (M, b)))) + (
        psutil.swap_memory()[1] / (1024**2)
    )

    # Stop timer
    # endTime = time.process_time()
    endTime = datetime.now()
    # print(endTime)
    # Calculate relative error
    rel_Error = np.linalg.norm(x - xe) / np.linalg.norm(xe)

    # Calculate execution time - memory usage
    exec_Time = endTime - startTime
    exec_Memory = endMemory - startMemory

    # Check relative error solution
    print("Relative error is: ", np.linalg.norm(x - xe) / np.linalg.norm(xe))

    # Check time execution
    print("Time execution of Cholesky: " + str((endTime - startTime)), " sec")

    # Check memory usage
    print("Memory used: " + str(endMemory - startMemory), " MB")

    # Check Operative System
    system = platform.system()

    return [system, dimension, rel_Error, exec_Time, exec_Memory]


def writeCSV():
    with open(path_data + "python_win.csv", "w", newline="\n") as ris:
        result = csv.writer(ris)
        result.writerow(header_csv)

        # for matrixList in ["cfd1.mtx", "cfd2.mtx", "ex15.mtx", "parabolic_fem.mtx", "shallow_water1.mtx"] :
        for filename in os.listdir(path_matrix):
            if filename.endswith(".mtx"):
                print("Leggo " + filename + " ...")
                # f = os.path.join(path_matrix, filename)
                [
                    system,
                    dimension,
                    rel_Error,
                    exec_Time,
                    exec_Memory,
                ] = calculateFunction(filename)
                # Write on csv file
                result.writerow(
                    [
                        "Python",
                        system,
                        filename,
                        dimension,
                        rel_Error,
                        exec_Time,
                        exec_Memory,
                    ]
                )


if __name__ == "__main__":
    writeCSV()
