import os
import sys
import pandas as pd
import numpy as np
import pickle
from src.constants import *

def load_and_save(category, filename, dataset, dataset_folder):
    temp = np.genfromtxt(os.path.join(dataset_folder, category, filename),
                         dtype=np.float64,
                         delimiter=',')
    print(dataset, category, filename, temp.shape)
    with open(os.path.join(output_folder, f"SMD/{dataset}_{category}.pkl"), "wb") as file:
        pickle.dump(temp, file)

def load_data(dataset):
	folder = os.path.join(output_folder, dataset)
	os.makedirs(folder, exist_ok=True)
	if dataset == 'synthetic':
		train_file = os.path.join(data_folder, dataset, 'synthetic_data_with_anomaly-s-1.csv')
		test_labels = os.path.join(data_folder, dataset, 'test_anomaly.csv')
		dat = pd.read_csv(train_file, header=None)
		split = 10000
		train = dat.values[:, :split].reshape(split, -1)
		test = dat.values[:, split:].reshape(split, -1)
		lab = pd.read_csv(test_labels, header=None)
		lab[0] -= split
		labels = np.zeros(test.shape)
		for i in range(lab.shape[0]):
			labels[lab.values[i][0], lab.values[i][1:]] = 1
		for file in ['train', 'test', 'labels']:
			with open(os.path.join(folder, f'{file}.pkl'), 'wb') as f:
				pickle.dump(eval(file), f)
	elif dataset == 'SMD':
		dataset_folder = 'data/SMD'
		file_list = os.listdir(os.path.join(dataset_folder, "train"))
		for filename in file_list:
			if filename.endswith('.txt'):
				load_and_save('train', filename, filename.strip('.txt'), dataset_folder)
				load_and_save('test', filename, filename.strip('.txt'), dataset_folder)
				load_and_save('test_label', filename, filename.strip('.txt'), dataset_folder)
	else:
		raise Exception('Not Implemented')

if __name__ == '__main__':
	datasets = ['synthetic', 'SMD']
	commands = sys.argv[1:]
	load = []
	if len(commands) > 0:
		for d in commands:
			if d in datasets:
				load_data(d)
	else:
		print("Usage: python preprocess.py <datasets>")
		print("where <datasets> is space separated list of ['synthtic', 'SMD']")