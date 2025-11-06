"""
    coding: utf-8
    Project: dwm_atlas_seperate
    File: cluster_end_points_decode.py
    Author: xieyu
    Date: 2025/8/14 21:29
    IDE: PyCharm
"""
import json

import pandas as pd
from joblib import Memory
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from step9.neurosynth_ana.utils import write_dict_2_json
import re

mem = Memory(location='/tmp/neurovault_analysis/cache')


def url_get(url):
    request = Request(url)
    response = urlopen(request)
    return response.read()


def get_neurosynth_terms(combined_df):
    """ Grab terms for each image, decoded with neurosynth"""
    terms = list()
    from sklearn.feature_extraction import DictVectorizer
    vectorizer = DictVectorizer()
    image_ids = list()
    for row in combined_df.iterrows():
        image_id = row[1]['image_id']
        image_ids.append(int(image_id))
        # print "Fetching terms for image %i" % image_id
        image_url = row[1]['url_image'].split('/')[-2]

        try:
            elevations = mem.cache(url_get)(
                        'http://neurosynth.org/decode/data/?neurovault=%s'
                        % image_url)
            data = json.loads(elevations)['data']
            data = dict([(i['analysis'], i['r']) for i in data])
        except HTTPError:
            data = {}
        terms.append(data)
    X = vectorizer.fit_transform(terms).toarray()
    term_dframe = dict([('neurosynth decoding %s' % name, X[:, idx])
                        for name, idx in vectorizer.vocabulary_.items()])
    term_dframe['image_id'] = image_ids

    return pd.DataFrame(term_dframe)
# "https://neurosynth.org/decode/?url=http://neurovault.org/media/images/21680/ArcuateFasciculus_Left.nii.nii.gz"

def get_neurosynth_decode(url, out_path):
    elevations = mem.cache(url_get)(f'https://neurosynth.org/decode/?url={url}')

    match = re.search(r"image_id\s*=\s*['\"]([a-f0-9]{32})['\"]", elevations.decode('utf-8'))
    if match:
        image_id = match.group(1)
        print("Found image_id:", image_id)
    else:
        print("image_id not found")
        return

    data_elevation = mem.cache(url_get)(f"https://neurosynth.org/api/decode/{image_id}/data/")

    # print(data_elevation)

    data = json.loads(data_elevation)

    write_dict_2_json(data, out_path)

    # print(elevations[:500])
    # data = json.loads(elevations)
    # print(data)
    # write_dict_2_json(data, out_path)


def main():

    # url = "http://neurovault.org/media/images/21680/ArcuateFasciculus_Left.nii.nii.gz"

    # url = "http://neurovault.org/media/images/21680/CorticoSpinalTract_Left.nii.nii.gz"
    # out_path = "/media/UG1/xieyu/CST_left_decode_results.json"
    # get_neurosynth_decode(url, out_path)

    pass


if __name__ == '__main__':
    main()

