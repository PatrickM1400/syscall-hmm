from os import listdir

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
        cluster_list = [pathname + filename + "\n" for filename in filenames if filename.startswith(cluster)]
        new_filenames = [filename for filename in filenames if not filename.startswith(cluster)]
        filenames = new_filenames

        cluster_filename = cluster + ".txt"
        with open(cluster_prefix+cluster_filename, "w") as file:
            file.writelines(cluster_list)

    # cluster_files = listdir(cluster_prefix)
    # for cluster_file in cluster_files:
    #     with open(cluster_prefix+cluster_file, "r") as cfile:
    #         logs = cfile.readlines()
    #         print(len(logs))


prefix = "./dongting/abnormal_data/"
clusters = ["sy_BUG__MAX_STACK_TRACE_ENTRIES_too_low", "sy_memory_leak_in_kobject_set_name_vargs"]
cluster_prefix = "./clusters/"
cluster_list = "cluster_list.txt"
cluster_data(prefix, clusters, cluster_prefix, cluster_list)