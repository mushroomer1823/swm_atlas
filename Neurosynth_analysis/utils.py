"""
    coding: utf-8
    Project: dwm_atlas_seperate
    File: utils.py
    Author: xieyu
    Date: 2025/8/14 15:05
    IDE: PyCharm
"""
import json

from pynv import Client


def get_api():
    token = get_token()
    api = Client(access_token=token)
    return api


def get_token():
    return ""


def create_collection(api, collection_name):
    collection = api.create_collection(collection_name)
    return collection


def get_collection(api, collection_id):
    collection = api.get_collection(collection_id=collection_id)
    return collection


def add_image(api, image_path, collection_id, name):
    image = api.add_image(
        collection_id,
        image_path,
        name=name,
        modality='Other',
        map_type='R',
        target_template_image='MNI152NLin2009cAsym',
        number_of_subjects=171,
        cognitive_paradigm_cogatlas="None",
        analysis_level="M"
        # custom_metadata_field=42
    )
    return image


def write_dict_2_json(dict_to_write, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(dict_to_write, f, ensure_ascii=False, indent=4)


def read_json(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


