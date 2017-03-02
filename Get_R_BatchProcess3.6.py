import os
import gc
import time
import numpy
from scipy import io
from microwave import Get_R_parallel

M = 1
N = 4000000
Channel_num = 25

time_start = time.time()
Path = r"D:\dou\doupy\interference\data\point_source"

if os.path.isdir(Path):
    pathDir = os.listdir(Path)
    k = 0
    for files in pathDir:
        k += 1
        subpath = os.path.join('%s/%s' % (Path, files))
        m = N * M
        n = Channel_num + 3
        all_data = numpy.zeros([m, n])
        Sample1_I = numpy.zeros(m)
        Sample2_I = numpy.zeros(m)
        Sample3_I = numpy.zeros(m)
        Sample4_I = numpy.zeros(m)
        File = os.listdir(subpath)
        for i in range(7):
            file_1 = os.path.join('%s/%s' % (subpath, File[i]))
            with open(file_1, 'rb') as f:
                for p in range(M):
                    Sample1_I[(p * N):((p + 1) * N)] = list(map(lambda x: (x + 128) % 256 - 128, list(f.read(N))))
                    Sample2_I[(p * N):((p + 1) * N)] = list(map(lambda x: (x + 128) % 256 - 128, list(f.read(N))))
                    Sample3_I[(p * N):((p + 1) * N)] = list(map(lambda x: (x + 128) % 256 - 128, list(f.read(N))))
                    Sample4_I[(p * N):((p + 1) * N)] = list(map(lambda x: (x + 128) % 256 - 128, list(f.read(N))))
            file_2 = os.path.join('%s/%s' % (subpath, File[i + 7]))
            with open(file_2, 'r') as f:
                ChannelNo = 0
                for line in f.readlines():
                    ChannelNo += 1
                    index = line.index('_')
                    offset = float(line[0:index - 1])
                    gain = float(line[index + 1:])
                    exec('Sample' + str(ChannelNo) + '_I=Sample' + str(ChannelNo) + '_I*gain+offset')
                    exec('all_data[:,4 * i + ChannelNo-1]' + '=Sample' + str(ChannelNo)
                         + '_I-numpy.mean(Sample' + str(ChannelNo) + '_I)')
        all_data[:, Channel_num + 1] = [None]
        all_data[:, Channel_num + 1] = [None]
        all_data[:, Channel_num + 1] = [None]

        del Sample1_I, Sample2_I, Sample3_I, Sample4_I
        gc.collect()
        R_inverse_matrix_ = Get_R_parallel.Get_R_parallel(Channel_num, all_data)
        Rpath = os.path.join('%s/%s' % (subpath, 'R2.mat'))
        io.savemat(Rpath, {'array': R_inverse_matrix_})
print(time.time() - time_start)
