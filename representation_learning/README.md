# Representation Learning 

This folder contains code to obtain the representations (via a pretrained Resnet-152 on ImageNet) of the VisualSem data as well as the MSCOCO images and their similarities. Additionally, some analysis is also available as well as visualization code.

## Data
This repository requires two datasets to run. The first one being the MSCOCO dataset and the other VisualSem. 

- To obtain the MSCOCO training data, follow this [link](http://cocodataset.org/#download
).
- The VisualSem data is currently not accessible, __we will update this as soon as possible__.

## Environment 
Please follow the general README of this repository for the environment. 


# Usage 
We assume that you are interesting in either getting the representation of the nodes in VisualSem or want to find similar VisualSem nodes to MSCOCO images. 

To obtain the average representations of the images for each node, run the following. __Please note that this can take some time, in our case ~15h.__
  ```python get_reps_nodes.py --batch your_batch_size --nodes_file where_nodes_stored --images_folder where_images_stored --store_matrix where_to_store_representations```

To obtain nodes (i.e a top 50 referenced by their numbers) from VisualSem that are most similar to a set of MSCOCO images, run the following. 
  ```python get_top_n_sim.py --store_matrix where_representations_stored --train_mscoco where_mscoco_ims_stored --store_dicts where_to_store_top_n```

# Examples
If you are interested in some examples, please check the representation_analysis folder. Here, we showcase for several distance measures as well as different representation sizes some related VisualSem nodes to a few MSCOCO images. 
