import os
import argparse
import json
import requests


ENV_FILE = open('.env.development')
ENV = json.load(ENV_FILE)
ENV_FILE.close()


def __fetch_feature(id):
    url = ENV['ASF_LPCLOUD_SEARCH_URL'] # https://cmr.earthdata.nasa.gov/stac/LPCLOUD/search

    payload = {
        'collections': ENV['ASF_HLS_COLLECTION'], # HLSL30.v2.0, HLSS30.v2.0
        'limit': 1,
        'ids': [id]
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request('POST', url, headers=headers, data=json.dumps(payload))
    
    if response.status_code != 200:
        print('ERROR: Response code {}'.format(response.status_code))
        return None
    
    data = response.json()
    
    if data['numberMatched'] == 0:
        return None
    
    return data['features'][0]


def __download_file(url, output):
    fn_local = '{}/{}'.format(output, url.split('/')[-1])
    headers = {
        'Authorization': 'Bearer {}'.format(ENV['ASF_TOKEN'])
    }

    if os.path.exists(fn_local):
        os.remove(fn_local)

    with requests.get(url, headers=headers, stream=True) as response:
        response.raise_for_status()

        with open(fn_local, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    return fn_local


def download_feature_bands(feature, bands, output):
    files = []
    
    for band in bands:
        if band in feature['assets']:
            files.append(__download_file(feature['assets'][band]['href'], output))
    
    return files


if __name__ == '__main__':
    print('Started program.\n')
    # python src/app.py HLS.L30.T10SGJ.2022332T183939.v2.0 B01,B03

    print('Reading arguments...')
    parser = argparse.ArgumentParser(prog='SatDownload')
    parser.add_argument('id')
    parser.add_argument('bands')
    parser.add_argument('--output', default='output')
    args = parser.parse_args()
    
    id = args.id
    bands = args.bands.split(',')
    output = args.output

    print('Fetching bands \'{}\' for granule \'{}\''.format(bands, id))
    print('Storing files in \'{}\' folder'.format(output))

    feature = __fetch_feature(id)
    
    if feature == None:
        print('ERROR: Feature with ID \'{}\' was not found in HLS collection.'.format(id))
        exit()
    
    print('Found feature, downloading bands...')
    download_feature_bands(feature, bands, output)

    print('\nComplete!')
