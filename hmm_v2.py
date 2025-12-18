from hmmlearn.hmm import CategoricalHMM
import numpy as np
from syscall_nums import * 
import pickle
from os import listdir

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

        # data_length = len(data)
        # if data_length > MAX_DATA_LENGTH:
        #     loops = int(data_length / MAX_DATA_LENGTH)
        #     remainder = data_length % MAX_DATA_LENGTH
        #     for i in range(loops):
        #         data_seg = data[i*MAX_DATA_LENGTH:i*MAX_DATA_LENGTH + MAX_DATA_LENGTH]
        #         hmm.fit(data_seg)
        #     hmm.fit(data[loops*MAX_DATA_LENGTH:])
        # else:
    
    arrays = [np.array(data[i:i + MAX_DATA_LENGTH]).reshape(-1,1) for i in range(0, len(data), MAX_DATA_LENGTH)]
    for array in arrays:
        print("Fitting one array")
        hmm.fit(array)

    with open(output, "wb") as f: pickle.dump(hmm, f)

# Train all hmms 
def train_hmms():

    with open("./training_data/sy_BUG.txt", "r") as file:
        logs = file.readlines()
        logs = [log.rstrip() for log in logs]

    train_hmm(logs, "", "sy_BUG.pkl", 50)

def test_hmm(files, prefix, input_hmm):

    with open(input_hmm, "rb") as file:
        hmm = pickle.load(file)
    
    for file in files:
        filename = prefix + file
        with open(filename, "r") as f:
            line = f.readline()
            data = np.array([syscall_nums[name] for name in line.split('|')]).reshape(-1, 1)

        x = data
        print("Testing on {}".format(file))
        print(hmm.bic(x)/len(x))



logs = ["dongting/abnormal_data/kernel_v510-299/sy_BUG__unable_to_handle_kernel_NULL_pointer_dereference_in_hci_uart_set_flow_control_POC2.log"]
prefix = ""
normal_files = ["dongting/normal_data/glibc/sy_atest-exp.log"]
abnormal_files = ["dongting/abnormal_data/kernel_v510-299/sy_BUG__using___this_cpu_read___in_preemptible_code_in_ip6_finish_output_POC5.log"]
# print(logs)
hmm_filename = "hmm_v2.pkl"


train_hmms()

# train_hmm(logs, prefix, hmm_filename)
# test_hmm(normal_files, prefix, hmm_filename)
# test_hmm(abnormal_files, prefix, hmm_filename)