from hmmlearn.hmm import CategoricalHMM
import numpy as np
from syscall_nums import * 
import pickle

# Train one hmm based on one cluster of syscall sequences
def train_hmm(files, output):

    hmm = CategoricalHMM(n_components=50, n_features=398) # 50 is constant that should be changed
    # print(testing.startprob_.shape)

    for file in files:
        with open(file, "r") as f:
            line = f.readline()
            data = np.array([syscall_nums[name] for name in line.split('|')]).reshape(-1, 1)

        hmm.fit(data)

    with open(output, "wb") as f: pickle.dump(hmm, f)



# training = CategoricalHMM(n_components=50, n_features=398)
# # print(testing.startprob_.shape)

# abnormal_file = './dongting/Abnormal_data/kernel_v500-289/sy_BUG__MAX_STACK_TRACE_ENTRIES_too_low__POC7.log'
# normal_file = './dongting/Normal_data/glibc 2884/sy_annexc.log'
# normal_file2 = './dongting/Normal_data/glibc 2884/sy_argp-test.log'

# with open(normal_file, "r") as f:
#     line = f.readline()
#     data = np.array([syscall_nums[name] for name in line.split('|')]).reshape(-1, 1)

# training.fit(data)

# print(training.startprob_)
# print(training.transmat_)
# print(training.emissionprob_)

# with open("hmm.pkl", "wb") as f: pickle.dump(training, f)

# with open("hmm.pkl", "rb") as bytes:
#     new_training = pickle.load(bytes)

# with open(normal_file2, "r") as f:
#     line = f.readline()
#     data = np.array([syscall_nums[name] for name in line.split('|')]).reshape(-1, 1)


# print(new_training.bic(data))

# print(new_training.startprob_)
# print(new_training.transmat_)
# print(new_training.emissionprob_)

# x = np.array([1,2,3,4,5,1,2,3,4,5,1,2,3,4,5]).reshape(-1, 1)
# y = np.array([1,2,3,4,4,2,2,3,4,5,1,2,4,4,5]).reshape(-1, 1)
# testing.fit(x)
# testing.fit(y)
# print(testing.startprob_.shape)
# print(testing.transmat_.shape)
# print(testing.emissionprob_.shape)
# print(type(testing)   )
# hidden_state = np.array([1,2,3,4,4]).reshape(-1,1)
# print(testing.bic(hidden_state))