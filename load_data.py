import os
import random
import numpy as np
import pandas as pd

class LoadData(object):

    _data_file_list = None
    _current_file_index = 0
    _extract_data_size = 0
    _class_num = 0
    _epoch = 0

    def __init__(self, data_path, time_step, class_num):
        if not os.path.exists(data_path):
            print('%s is not found'%(data_path))
            raise FileExistsError
        self._time_step = time_step
        self._extract_data_size = self._time_step
        self._class_num = class_num
        self._data_file_list = [os.path.join(data_path, file) for file in os.listdir(data_path)]

    def get_next_batch(self, batchsize):
        if self._current_file_index+1 == len(self._data_file_list):
            self._current_file_index = 0
            self._epoch += 1

        data = pd.read_csv(self._data_file_list[self._current_file_index])
        self._current_file_index += 1
        data_size = len(data.acc_x.values)

        train_x = []
        label_y = []
        for i in range(batchsize):
            start = random.randint(1, data_size-self._extract_data_size)
            train_x.append(data.iloc[start:start+self._extract_data_size, 0:6].values)
            label = [[0 for i in range(self._class_num)] for _ in range(self._extract_data_size)]

            for s in range(self._extract_data_size):
                j = data.iloc[start + s:start + s + 1, 6].values[0]
                label[s][j] = 1
            label_y.append(label)

        return np.array(train_x), np.array(label_y)

    @property
    def epoch(self):
        return self._epoch

if __name__ == '__main__':
    data = LoadData('./dataset/train/', time_step=3, class_num=11)
    x,y=data.get_next_batch(2)
    print(x.shape)
    print(y.shape)