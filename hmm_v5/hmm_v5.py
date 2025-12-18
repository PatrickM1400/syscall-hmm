# This is small training set using window sliding value of 3



from hmmlearn.hmm import CategoricalHMM
import numpy as np
from syscall_nums import * 
import pickle as pkl
from os import listdir
import os
import math



MAX_DATA_LENGTH = 10000
NUM_SYSCALLS = 398

def window_val(syscall_sequence, window_size, i):
    output = syscall_sequence[i]
    for idx in range(1,window_size):
        output += syscall_sequence[i + idx] * math.pow(NUM_SYSCALLS, idx)
    return output
    

def transform_data(syscall_sequence, window_size, pickle_name):
    sliding_windows_vals = [window_val(syscall_sequence, window_size, i) for i in range(0, len(syscall_sequence)-window_size+1)]
    window_value_transformation = {}
    # num_unique = set()
    new_val = 1
    for val in sliding_windows_vals:
        if val not in window_value_transformation:
            window_value_transformation[val] = new_val
            new_val += 1
        # num_unique.add(val)

    sliding_windows_vals = [window_value_transformation[val] for val in sliding_windows_vals]

    transformation_filename = pickle_name[:-4] + "_transformation.txt"

    with open(transformation_filename, "wb") as transform_file:
        pkl.dump(window_value_transformation, transform_file)
    # print(len(num_unique))
    # print(new_val)
    return sliding_windows_vals
    


# Train one hmm based on one cluster of syscall sequences
def train_hmm(files, prefix, output, n_components):

    hmm = CategoricalHMM(n_components=n_components) # 50 is constant that should be changed
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

    if len(data) > MAX_DATA_LENGTH: # Cap maximum data length if single file is very large
        data = data[:MAX_DATA_LENGTH]

    # arrays = [np.array(data[i:i + MAX_DATA_LENGTH]).reshape(-1,1) for i in range(0, len(data), MAX_DATA_LENGTH)]
    data =  transform_data(data, 3, output)
    # print(data)
    hmm_data = np.array(data).reshape(-1,1)
    # print(hmm_data)
    # for array in arrays:
    # print("Fitting one array")
    hmm.fit(hmm_data)

    with open(output, "wb") as f: pkl.dump(hmm, f)

# Train all hmms hmm_v4
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
        train_hmm(logs, "", pickle_name, 10)

def test_hmms(testing_filename, testing_output, alpha):
    window_size = 3

    cluster_names = listdir("./training_data")
    with open(testing_output, "w") as bic_file:
        bic_file.writelines("cluster:log_filename:bic\n")
        for cluster_name in cluster_names:
            print("Testing on cluster {}".format(cluster_name))
            pickle_name = cluster_name[:-4] + ".pkl"
            with open(pickle_name, "rb") as file:
                hmm = pkl.load(file)

            transformation_filename = pickle_name[:-4] + "_transformation.txt"
            window_value_transformation = {}
            with open(transformation_filename, "rb") as transform_file:
                window_value_transformation = pkl.load(transform_file)
                # print("Loaded window_value_transformation")

            with open(testing_filename, "r") as testing_file:
                logs = testing_file.readlines()

            for log in logs:
                with open(log.rstrip(), "r") as f:
                    line = f.readline()
                    syscall_sequence = [syscall_nums[name] for name in line.split('|')]

                old_bic = 0
                bic_file.writelines(cluster_name + ":" + log.rstrip() + ":")
                # data = [data[i] + data[i+1] * NUM_SYSCALLS + data[i+2] * math.pow(NUM_SYSCALLS, 2) for i in range(0,len(data)-2)]
                sliding_windows_vals = [window_val(syscall_sequence, window_size, i) for i in range(0, len(syscall_sequence)-window_size+1)]
                sliding_windows_vals = [window_value_transformation[val] if val in window_value_transformation else -1 for val in sliding_windows_vals] # Reduce number of states
                # print(sliding_windows_vals)
                for elem0, elem1 in zip(sliding_windows_vals[:1000], sliding_windows_vals[:1000][1:]):
                    data = np.array([elem0, elem1]).reshape(-1, 1)
                    # print(data)
                    # print("")

                    try:
                        bic_inv = 1/hmm.bic(data)
                    except:
                        bic_inv = 0

                    old_bic = old_bic * (1-alpha) + bic_inv * alpha
                    bic_file.writelines(str(old_bic) + ",")
                bic_file.writelines("\n")



prefix = ""
normal_files = ["dongting/normal_data/glibc/sy_atest-exp.log"]
abnormal_files = ["dongting/abnormal_data/kernel_v510-299/sy_BUG__using___this_cpu_read___in_preemptible_code_in_ip6_finish_output_POC5.log"]
# print(logs)
testing_filename_normal = "testing_files_normal.txt"
testing_filename_abnormal = "testing_files_abnormal.txt"
testing_output_normal = "testing_bic_normal.txt"
testing_output_abnormal = "testing_bic_abnormal.txt"
alpha = 0.5 # Higher alpha stands for larger weight on most recent bic

# train_hmms()

test_hmms(testing_filename_normal, testing_output_normal, alpha)
test_hmms(testing_filename_abnormal, testing_output_abnormal, alpha)

# test_hmm(normal_files, prefix, hmm_filename)
# test_hmm(abnormal_files, prefix, hmm_filename)