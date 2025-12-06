import pandas as pd

syscalls = pd.read_table('./dongting/syscall_64_clean.tbl', delimiter='\t', header=None) 
idx = 0
for syscall in syscalls.iloc[:,2]:
    print('"' + syscall + '":' + str(idx), ",")
    idx += 1