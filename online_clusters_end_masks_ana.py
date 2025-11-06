"""
    coding: utf-8
    Project: dwm_atlas_seperate
    File: online_clusters_end_masks_ana.py
    Author: xieyu
    Date: 2025/8/19 17:07
    IDE: PyCharm
"""

import os
import time

from tqdm import tqdm

from step9.neurosynth_ana.utils import read_json
from step9.neurosynth_ana.cluster_end_points_decode import get_neurosynth_decode


def decode_single_cluster(json_path, out_path):
    cur_dict = read_json(json_path)
    cur_url = cur_dict["url"]
    get_neurosynth_decode(cur_url, out_path)


def main():

    network_types = ["7", "17"]

    for network_type in network_types:

        url_base_path = f"/media/UG1/xieyu/hyf_clustering_results/{network_type}Parcels/cluster_upload_urls/"

        out_base_path = f"/media/UG1/xieyu/hyf_clustering_results/{network_type}Parcels/cluster_end_points_decode_results/"
        if not os.path.exists(out_base_path):
            os.makedirs(out_base_path)

        cluster_names1 = [name for name in os.listdir(url_base_path) if os.path.isdir(os.path.join(url_base_path, name))]

        for cluster_name1 in tqdm(cluster_names1):
            cur_url_base_path = os.path.join(url_base_path, cluster_name1)
            cur_out_base_path = os.path.join(out_base_path, cluster_name1)
            if not os.path.exists(cur_out_base_path):
                os.makedirs(cur_out_base_path)

            cluster_names2 = os.listdir(cur_url_base_path)

            for cluster_name2 in tqdm(cluster_names2):
                cur_json_path = os.path.join(cur_url_base_path, cluster_name2)
                cur_out_path = os.path.join(cur_out_base_path, cluster_name2)
                if not os.path.exists(cur_out_path):
                    decode_single_cluster(cur_json_path, cur_out_path)
                    time.sleep(1)
            # break


if __name__ == '__main__':
    main()
