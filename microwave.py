from scipy import fftpack
import numpy
from multiprocessing.dummy import Pool

def Get_R_parallel(num, data):
    R_matrix = numpy.zeros([num, num], complex)
    p = Pool(4)
    for v in range(num):
        hilbert_v = p.starmap(complex, zip(data[:, v], -fftpack.hilbert(data[:, v])))
        R_matrix[v, :] = p.map(numpy.mean, [hilbert_v * data[:, l] for l in range(num)])
    p.close()
    p.join()
    return R_matrix