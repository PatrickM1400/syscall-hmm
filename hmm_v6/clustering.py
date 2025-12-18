from os import listdir
from random import sample

def cluster_data(prefix, clusters, cluster_prefix, cluster_list):

    # Get list with all filenames
    versions = listdir(prefix)
    filenames = []
    for version in versions:
        pathname = prefix + version + "/"
        filenames += (listdir(pathname))

        with open(cluster_list, "r") as cluster_file:
            clusters = cluster_file.readlines()
            clusters = [cluster.rstrip() for cluster in clusters if cluster != ""]

        for cluster in clusters:
            log_list = [pathname + filename + "\n" for filename in filenames if filename.startswith(cluster)]
            new_filenames = [filename for filename in filenames if not filename.startswith(cluster)]
            filenames = new_filenames

            cluster_filename = cluster + ".txt"
            with open(cluster_prefix+cluster_filename, "a") as file:
                file.writelines(log_list)

def create_training_set(cluster_prefix, training_prefix):

    clusters = listdir(cluster_prefix)
    for cluster in clusters:
        cluster_pathname = cluster_prefix + cluster
        print(cluster_pathname)
        with open(cluster_pathname, "r") as cluster_file:
            logs = cluster_file.readlines()

        if len(logs) > 100:
            training_logs = sample(logs, 100)
            print(training_logs)
        else:
            training_logs = logs
        
        training_pathname = training_prefix + cluster
        with open(training_pathname, "w") as training_file:
            training_file.writelines(training_logs)

def create_testing_set(cluster_prefix, dongting_normal_data, testing_filename_normal, testing_filename_abnormal):

    with open(testing_filename_abnormal, "w") as testing_file_abnormal:
        clusters = listdir(cluster_prefix)
        for cluster in clusters:
            cluster_pathname = cluster_prefix + cluster
            # print(cluster_pathname)
            with open(cluster_pathname, "r") as cluster_file:
                logs = cluster_file.readlines()


            num_files_per_cluster = 6
            if len(logs) <= num_files_per_cluster:
                testing_log = sample(logs, len(logs))
            else:
                testing_log = sample(logs, num_files_per_cluster)

            testing_file_abnormal.writelines(testing_log)

    with open(testing_filename_normal, "w") as testing_file_normal:
        normal_data_groups = listdir(dongting_normal_data)
        for normal_data_group in normal_data_groups:
            group_pathname = dongting_normal_data + normal_data_group
            # print(group_pathname)
            logs = listdir(group_pathname)

            testing_log = sample(logs, 25)
            testing_log = [group_pathname + '/' + log + '\n' for log in testing_log]
            # print(testing_log)

            testing_file_normal.writelines(testing_log)

prefix = "./dongting/abnormal_data/"
dongting_normal_data = "../dongting/normal_data/"
clusters = ["sy_BUG__MAX_STACK_TRACE_ENTRIES_too_low", "sy_memory_leak_in_kobject_set_name_vargs"]
cluster_prefix = "./clusters/"
training_prefix = "./training_data/"

# testing_prefix = "./testing_data/"
testing_filename_normal = "testing_files_normal.txt"
testing_filename_abnormal = "testing_files_abnormal.txt"
cluster_list = "cluster_list.txt"

# cluster_data(prefix, clusters, cluster_prefix, cluster_list)
# create_training_set(cluster_prefix, training_prefix)
create_testing_set(cluster_prefix, dongting_normal_data, testing_filename_normal, testing_filename_abnormal)