import urllib.request
import json
from utils import from_lemma_to_ids, create_folder, from_synsetID_to_images, get_edges_from_synset, return_core_graph, process_sense_info, edge_information, process_imgs, get_key
from tqdm import tqdm
import time
import networkx as nx
#%matplotlib inline
#import matplotlib.pyplot as plt
import numpy as np
from collections import Counter, defaultdict
import os
import subprocess

nodes_file = "data/nodes_180k.json"
edges_file = "data/edges_180k.json"
sources_file = "data/img_sources.json"
store_steps_nodes = "data/testing/n1000_15_" # Where files are stored, also indicated in extract_nodes.py
k = 50
min_ims = 0
which_iter = 4 # For 100k nodes, this is 3, whereas for 180k nodes it is 4

with open('data/nodes_1000.json', 'r') as f:
    nodes = json.loads(f.read())

def process_sense_info_n(id_syn, key=None):
    synset_info, synset_images = from_synsetID_to_images(id_syn, key)
    senses = list(set([entry["properties"]["fullLemma"] for entry in synset_info["senses"]]))
    glosses = list(set([entry["gloss"] for entry in synset_info["glosses"]]))
    main_sense = synset_info["mainSense"]
    ims = [img["url"] for img in synset_images]
    source_ims = {img["url"].split("/")[-1]: img["urlSource"] for img in synset_images}
    #synset_id = id_syn
    #if "wn:" in id_syn:
    #    synset_id = list(set([sen["properties"]["synsetID"]["id"] for sen in synset_info["senses"]]))[0]
    return senses, glosses, main_sense, ims, source_ims

def get_nodes(file_name, current_nodes):
    with open(file_name + "_lts", "r") as f:
        mapping = json.loads(f.read())
    with open(file_name + ".sorted", "r") as f:
        new_lines = [l.split() for l in f.read().split("\n")][:-1]
    print("amount new extra nodes: ", str(len(new_lines)))
    for line in new_lines:
        current_nodes.add(mapping[line[0]])
    return current_nodes

if __name__ == "__main__":
    curr_n = set(nodes.keys())
    for i in range(which_iter + 1):
        complete_line = store_steps_nodes + str(k) + "_" + str(min_ims) + "_r" + str(i)
        print("Previous unique nodes: ", str(len(curr_n)))
        curr_n = get_nodes(complete_line, curr_n)
        print("Next unique nodes: ", str(len(curr_n)))

    # For the images and the nodes
    img_dict = {}
    nodes_dict = {}
    img_sources = {}
    for n in tqdm(curr_n, mininterval=10):
        senses, glosses, main_sense, ims, source_ims = process_sense_info_n(n)
        img_dict[n] = ims
        # gl = glosses, ms = main sense, se=senses
        nodes_dict[n] = {"gl": glosses, "ms": main_sense, "se": senses}
        img_sources[n] = source_ims

    with open(nodes_file, "w") as f:
        json.dump(nodes_dict, f)

    with open(sources_file, "w") as f:
        json.dump(img_sources, f)

    # Get the edges
    edges = []
    for i in [which_iter]:
        complete_line = store_steps_nodes + str(k) + "_" + str(min_ims) + "_r" + str(i) + "_edges"
        with open(complete_line, "r") as f:
            edg = json.loads(f.read())
        edges.append(edg)

    # restore edges
    all_edges = defaultdict(list)
    r_id = 0
    for edg in edges:
        for key, value in tqdm(edg.items(), mininterval=10):
            for rel, s in value:
                all_edges[key].append({"s": s, "r": rel, "r_id": r_id})
                r_id += 1
    # remove possible duplicates
    all_edges = {key:[dict(t) for t in {tuple(d.items()) for d in value}] for key, value in all_edges.items()}
    with open(edges_file, "w") as f:
        json.dump(all_edges, f)
