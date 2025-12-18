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

def create_testing_set(cluster_prefix, training_filename):

    with open(training_filename, "w") as training_file:
        clusters = listdir(cluster_prefix)
        for cluster in clusters:
            cluster_pathname = cluster_prefix + cluster
            print(cluster_pathname)
            with open(cluster_pathname, "r") as cluster_file:
                logs = cluster_file.readlines()

            testing_log = sample(logs, 1)
            training_file.writelines(testing_log)


prefix = "./dongting/abnormal_data/"
clusters = ["sy_BUG__MAX_STACK_TRACE_ENTRIES_too_low", "sy_memory_leak_in_kobject_set_name_vargs"]
cluster_prefix = "./clusters/"
training_prefix = "./training_data/"
# testing_prefix = "./testing_data/"
training_filename = "training_files.txt"
cluster_list = "cluster_list.txt"

# cluster_data(prefix, clusters, cluster_prefix, cluster_list)
# create_training_set(cluster_prefix, training_prefix)
create_testing_set(cluster_prefix, training_filename)