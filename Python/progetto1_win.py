import os
import csv
import time
import numpy as np
from scipy.io import mmread
from scipy.linalg import norm
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve
import psutil


def sparse_solve(A, b):
    start = time.perf_counter()
    x = spsolve(A, b)
    stop = time.perf_counter()
    fntime = stop - start
    erel = norm(x - xe, ord=2) / norm(xe, ord=2)

    return fntime, erel


path_matrix = "C:/Users/papad/Code/LinearSolver/Matrix MTX/"
path_data = "C:/Users/papad/Code/LinearSolver/Data/"

process = psutil.Process(os.getpid())
with open(path_data + "python_win.csv", "w+", newline="") as file:
    writer = csv.writer(file)
    # Header CSV
    writer.writerow(["Matrice", "Dimensione", "Tempo", "Memoria", "ErroreRelativo"])

    for filename in os.listdir(path_matrix):
        if filename.endswith(".mtx"):
            try:
                print("Leggo " + filename + " ...")

                # Leggo la matrice
                A = mmread(path_matrix + filename)
                A = csc_matrix(A)

                # Creo Array [1...1]
                size = A.shape[0]
                xe = np.ones(size)

                # Creo il vettore b
                b = A * xe
                print("Eseguo " + filename + " ...")

                # Solve
                [fntime, erel] = sparse_solve(A, b)

                # convert from byte to MB
                mem_usage = process.memory_info().peak_wset / 10**6
                writer.writerow([filename, size, fntime, mem_usage, erel])

            except MemoryError:
                    #Gestione dell'errore di memoria
                    print("Errore di memoria. Impossibile allocare risorse.")
            continue
