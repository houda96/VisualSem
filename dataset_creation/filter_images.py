import json
import sys
import hashlib
import glob
from tqdm import tqdm
from collections import defaultdict
import os
import magic
import networkx as nx

with open("data/hashes.json", "r") as f:
    hashes = json.loads(f.read())

with open("data/hashes_magic_dict.json", "r") as f:
    magic_dict = json.loads(f.read())

with open("data/nodes_180k.json", "r") as f:
    nodes_180k = json.loads(f.read())

with open("data/edges_180k.json", "r") as f:
    all_edges_180k = json.loads(f.read())

with open("marking_dict.json", "r") as f:
    marking_dict = json.loads(f.read())

if __name__ == "__main__":
    counts = {}
    for key in tqdm(nodes_180k.keys(), mininterval=10):
        if key in magic_dict.keys():
            imgs = set(magic_dict[key])
            counts[key] = len(imgs.intersection(good_imgs))
        else:
            counts[key] = 0
    edggs = {}
    to_use = set([key for key, value in counts.items() if value >= 4])
    for key, value in all_edges_180k.items():
        if key in to_use:
            l = []
            for entry in value:
                if entry["s"] in to_use:
                    l.append(entry)
            edggs[key] = l


    with open("data/nodes.json", "w") as f:
        json.dump(new_nodes, f)

    with open("data/edges.json", "w") as f:
        json.dump(to_use_edg, f)
