from hmmlearn.hmm import CategoricalHMM
import numpy as np
from syscall_nums import * 
import pickle
from os import listdir
import os
import math

MAX_DATA_LENGTH = 1000000

# Train one hmm based on one cluster of syscall sequences
def train_hmm(files, prefix, output, n_components):

    hmm = CategoricalHMM(n_components=n_components, n_features=398) # 50 is constant that should be changed
    # print(testing.startprob_.shape)
    data = []
    for file in files:
        filename = prefix + file
        with open(filename, "r") as f:
            line = f.readline()
            data += [syscall_nums[name] for name in line.split('|')]
        print("Training with {}".format(file))
        if len(data) > MAX_DATA_LENGTH: # Only perform 1-2 rounds of training
            break

    if len(data) > 2 * MAX_DATA_LENGTH: # Cap maximum data length if single file is very large
        data = data[:2 * MAX_DATA_LENGTH]

    arrays = [np.array(data[i:i + MAX_DATA_LENGTH]).reshape(-1,1) for i in range(0, len(data), MAX_DATA_LENGTH)]
    for array in arrays:
        print("Fitting one array")
        hmm.fit(array)

    with open(output, "wb") as f: pickle.dump(hmm, f)

# Train all hmms hmm_v3
def train_hmms():

    cluster_names = listdir("./training_data")
    for cluster_name in cluster_names:
        pickle_name = cluster_name[:-4] + ".pkl"
        # if pickle_name == 'sy_lost_connection.pkl' or pickle_name == 'sy_UBSAN.pkl' or pickle_name == 'sy_unregister_netdevice.pkl' or pickle_name == 'sy_WARNING.pkl':
        #     continue
        with open("./training_data/{}".format(cluster_name), "r") as file:
            logs = file.readlines()
            logs = [log.rstrip() for log in logs]
        print("Training on cluster {}".format(cluster_name))
        train_hmm(logs, "", pickle_name, 50)

def test_hmms(testing_filename, testing_output, alpha):

    cluster_names = listdir("./training_data")
    with open(testing_output, "w") as bic_file:
        bic_file.writelines("cluster:log_filename:bic\n")
        for cluster_name in cluster_names:
            print("Testing on cluster {}".format(cluster_name))
            pickle_name = cluster_name[:-4] + ".pkl"
            with open(pickle_name, "rb") as file:
                hmm = pickle.load(file)

            with open(testing_filename, "r") as testing_file:
                logs = testing_file.readlines()

            for log in logs:
                with open(log.rstrip(), "r") as f:
                    line = f.readline()
                    data = [syscall_nums[name] for name in line.split('|')]

                old_bic = 0
                bic_file.writelines(cluster_name + ":" + log.rstrip() + ":")
                for elem0, elem1 in zip(data[:1000], data[:1000][1:]):
                    data = np.array([elem0, elem1]).reshape(-1, 1)
                    bic_inv = 1/hmm.bic(data)
                    old_bic = old_bic * (1-alpha) + bic_inv * alpha
                    bic_file.writelines(str(old_bic) + ",")
                bic_file.writelines("\n")

                    


        # for file in files:
        #     filename = prefix + file
        #     with open(filename, "r") as f:
        #         line = f.readline()
        #         data = np.array([syscall_nums[name] for name in line.split('|')]).reshape(-1, 1)

        #     x = data
        #     print("Testing on {}".format(file))
        #     print(hmm.bic(x)/len(x))



prefix = ""
normal_files = ["dongting/normal_data/glibc/sy_atest-exp.log"]
abnormal_files = ["dongting/abnormal_data/kernel_v510-299/sy_BUG__using___this_cpu_read___in_preemptible_code_in_ip6_finish_output_POC5.log"]
# print(logs)
hmm_filename = "hmm_v3.pkl"
testing_filename_normal = "testing_files_normal.txt"
testing_filename_abnormal = "testing_files_abnormal.txt"
testing_output_normal = "testing_bic_normal.txt"
testing_output_abnormal = "testing_bic_abnormal.txt"
alpha = 0.1 # Higher alpha stands for larger weight on most recent bic

# train_hmms()
test_hmms(testing_filename_normal, testing_output_normal, alpha)
test_hmms(testing_filename_abnormal, testing_output_abnormal, alpha)

# test_hmm(normal_files, prefix, hmm_filename)
# test_hmm(abnormal_files, prefix, hmm_filename)