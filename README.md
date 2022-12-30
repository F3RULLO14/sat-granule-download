# Search, Download Granules

This script fetches and downloads bands of a COG from the LPCLOUD data center.

## Prerequisite

To run the script, important python libraries are required.

- requests

## How to

The script can be ran from the command line or included in a project as an import.

### Command line

The python script can be ran from the command line. Two arguments are required, an input and output file path, name.

`python src/app.py {granule_id} {bands}`

**Optional arguments** include `--output`.

Including `--output` tells the app where to download the granule bands to.

#### Example

*From README directory*

`python src/app.py HLS.S30.T11SKD.2022359T185809.v2.0 B01,B03 --output output`

The geotif (`output/HLS.S30.T11SKD.2022359T185809.v2.0.B01.tif`) was download by the above command.

<img src="output/HLS.S30.T11SKD.2022359T185809.v2.0.B01_screenshot.png" width="700">

### Imported

Once the script is copied over to your project or built/installed with python's wheel, you can access key functions to calculate difference values of multiple geotiffs.

To access, either:

`import app`

`from app import download_feature_bands`

Once imported, these two functions can be used to determine NDVI values.

#### Example Usage

```
import app
    
if __name__ == "__main__":
    feature = {...} #feature dict
    bands = ['B01', 'B03']
    app.download_feature_bands(feature, bands, output)
```

Further documentation is included on the functions.