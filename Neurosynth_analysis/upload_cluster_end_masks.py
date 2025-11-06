"""
    coding: utf-8
    Project: dwm_atlas_seperate
    File: upload_cluster_end_masks.py
    Author: xieyu
    Date: 2025/8/14 20:58
    IDE: PyCharm
"""
import os
import time

from tqdm import tqdm

from step9.neurosynth_ana.utils import get_collection, get_api, create_collection, add_image, write_dict_2_json, read_json


def main():

    api = get_api()

    network_types = ["7", "17"]

    for network_type in network_types:
        cur_collection_name = f"SWM_{network_type}Parcels"

        cur_mask_base_path = f"/media/UG1/xieyu/hyf_clustering_results/{network_type}Parcels/cluster_end_masks/"

        out_base_path = f"/media/UG1/xieyu/hyf_clustering_results/{network_type}Parcels/cluster_upload_urls/"
        if not os.path.exists(out_base_path):
            os.makedirs(out_base_path)

        cur_collection_json_path = os.path.join(out_base_path, "collection.json")

        if os.path.exists(cur_collection_json_path):
            cur_collection = read_json(cur_collection_json_path)
        else:
            cur_collection = create_collection(api, cur_collection_name)
            write_dict_2_json(cur_collection, cur_collection_json_path)

        cluster_names1 = os.listdir(cur_mask_base_path)

        for cluster_name1 in tqdm(cluster_names1):

            cur_out_base_path = os.path.join(out_base_path, cluster_name1)

            if not os.path.exists(cur_out_base_path):
                os.makedirs(cur_out_base_path)

            cluster_names2 = os.listdir(os.path.join(cur_mask_base_path, cluster_name1))

            cluster_names2 = [item.split(".")[0] for item in cluster_names2]

            for cluster_name2 in tqdm(cluster_names2):
                cur_out_path = os.path.join(cur_out_base_path, f"{cluster_name2}.json")

                if os.path.exists(cur_out_path):
                    continue

                cur_image_path = os.path.join(cur_mask_base_path, cluster_name1, f"{cluster_name2}.nii.gz")
                cur_image = add_image(api, cur_image_path, cur_collection["id"], f"{cluster_name1}-{cluster_name2}")
                cur_dict = {
                    'id': cur_image['id'],
                    'url': cur_image['file'],
                }

                write_dict_2_json(cur_dict, cur_out_path)
                time.sleep(1.5)
        #         break
        #     break
        # break


if __name__ == '__main__':
    main()
