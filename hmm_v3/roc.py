import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.axes as ax
import numpy as np


def split_list(entry):
    # Check if the entry is valid (not empty or NaN)
    if not entry or pd.isna(entry):
        return []
    # Split the string by comma and convert each part to a float
    return [float(x) for x in entry.split(',')[:-1]]

def generate_roc(testing_output_normal, num_per_normal_cluster, testing_output_abnormal, num_per_abnormal_cluster, roc_point_filename):
    df_normal = pd.read_csv(testing_output_normal, sep=":", converters={2: split_list})
    df_abnormal = pd.read_csv(testing_output_abnormal, sep=":", converters={2: split_list})
    file_list_normal = df_normal.head(num_per_normal_cluster)["log_filename"].values.tolist()
    file_list_abnormal = df_abnormal.head(num_per_abnormal_cluster)["log_filename"].values.tolist()

    base_thresholds = [1e-6, 1e-5]
    thresholds = [elem * (i/64.0) for elem in base_thresholds for i in range(64,640)]
    # print(thresholds)
    roc_points = []
    for threshold in thresholds:

        false_positives = 0.0
        for filename in file_list_normal:
            bic_lists_normal = df_normal.loc[df_normal["log_filename"] == filename]["bic"].values.tolist()

            for bic_list_normal in bic_lists_normal:
                # print(bic_list_normal)
                if max(bic_list_normal) > threshold:
                    false_positives += 1
                    break

        true_positives = 0.0
        for filename in file_list_abnormal:
            bic_lists_abnormal = df_abnormal.loc[df_abnormal["log_filename"] == filename]["bic"].values.tolist()

            for bic_list_abnormal in bic_lists_abnormal:
                # print(bic_list_abnormal)
                if max(bic_list_abnormal) > threshold:
                    true_positives += 1
                    break

        roc_points.append((false_positives/num_per_normal_cluster, true_positives/num_per_abnormal_cluster))

    with open(roc_point_filename, "w") as roc_file:
        roc_file.writelines(str(roc_points))

    # print(roc_points)
    x = [point[0] for point in roc_points[::-1]]
    y = [point[1] for point in roc_points[::-1]]
    plt.step(x, y)

    plt.axline([0, 0], [1, 1], color='red', linestyle='--')

    plt.savefig("roc.png")

def plot_roc(roc_points_filename):
    with open(roc_points_filename) as roc_file:
        roc_point_str = roc_file.readline()
    roc_point_str = roc_point_str[1:-1]
    roc_points = roc_point_str.split()
    roc_points = [(float(roc_points[i][1:-1]),float(roc_points[i+1][:-2])) for i in range(0,len(roc_points)-1,2)]

    print(roc_points)

    x = [point[0] for point in roc_points[::-1]]
    y = [point[1] for point in roc_points[::-1]]
    plt.step(x, y)

    plt.axline([0, 0], [1, 1], color='red', linestyle='--')

    plt.savefig("roc.png")
            
        

testing_output_normal = "testing_bic_normal.txt"
testing_output_abnormal = "testing_bic_abnormal.txt"
roc_points_filename = "roc_points.txt"

generate_roc(testing_output_normal, 100, testing_output_abnormal, 108, roc_points_filename)
# plot_roc(roc_points_filename)