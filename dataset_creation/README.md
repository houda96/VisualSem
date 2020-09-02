# Creating VisualSem

This repository contains code to re-create VisualSem.

## Disclaimer
VisualSem is obtained with the help of BabelNet, which follows a non-commercial license, hence why VisualSem follows that same license.

Moreover, it also involves many steps that takes time (days) and some manual checks for the paths, since these are constants at the top of the scripts.

## Data
Please follow the request information of this on our [paper GitHub](https://github.com/iacercalixto/visualsem).

## Environment
Please follow the general README of this repository for the environment.

# Usage
We assume that you want to re-create VisualSem.

Before you can start, you will have to have access to the BabelNet API (RESEARCH ONLY!). Go to [BabelNet](https://babelnet.org/), create an account and choose one of the two options; either obtain enough requests to be able to get all the amount of nodes or obtain the BabelNet indices and get the Java API working and make an end-point to it to access it http-like. Choose which-ever is preferable and change paths accordingly in the utils.py.

Besides having BabelNet configured, our image cleaning is done automatically with the pre-trained ResNet on imagi-filter. To obtain all this, we refer you to our [other GitHub project](https://github.com/houda96/imagi-filter). **NOTE: to do the image filtering in VisualSem, you have to have this.**

1. We start by extracting the nodes; please check the constants in the script and beware of longer runtimes.
  ```python extract_nodes.py```

2. Next, we will store the relations between the nodes. Make sure to check the constants again in the script. **Note: The file names will be used further down the pipeline.**
  ```python store_edg_info.py```

3. Now, we will obtain some additional images for the initial core, which can be extended if more nodes are desired to have images.
  ```python google_download.py```

4. Since we are dealing with many images, we first partition the images in chunks to be able to either run things in parallel or have in between breaks.
  ```python image_urls.py```

5. We then use [aria2](https://aria2.github.io/) via the command-line to download the images. These parameters have been optimized for our PC, please ensure that this is also suitable for the specs of your device.
  ```aria2c -i urls_file -x 16 -j 48 -t 5 --disable-ipv6 --connect-timeout=5```

6. We then start hashing the images to remove duplicates.
  ```python hash_exist_images.py```

7. We convert image types that cannot be processed further via Bash.
  ```./convert.sh```

8. We resize the images to reduce the space the images take in memory.
  ```python resizing.py```

9. The first filtering is done by checking whether the image files are correctly formatted; i.e. this step filters out ill-formatted image files.
```python list_good_bad_files.py```


10. This step classifies the images as being informative or not and ouputs json files for later filtering. The parser can take many arguments here. **NOTE: This part follows our imagi-filter model as explained at the start of this README**
  ```python forward_pass.py```

11. Now we filter out the images that are not useful in VisualSem; we do not remove them, but simply do not keep them in the information system itself so that even non-informative images can be excessed if necessary.
```python filter_images.py```
