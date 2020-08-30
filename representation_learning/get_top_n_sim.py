import torch
import torch.nn as nn
import json
import argparse
from torchvision import transforms
from PIL import Image
from tqdm import tqdm
from cnn import CNN
import h5py
import os
import glob
from collections import defaultdict

normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
transform = transforms.Compose([transforms.RandomResizedCrop(224), transforms.RandomHorizontalFlip(),
                transforms.ToTensor(), normalize])

AMOUNT_REP_FILES = 11
BASE_NAME = "matrix_representations"
SMOOTH_L1 = nn.SmoothL1Loss(reduction='none')

def map_mscoco_number(folder_mscoco, storage):
    complete_filename = storage + "mscoco_mapping.json"
    # If file exists already, use that mapping
    if os.path.exists(complete_filename):
        with open(complete_filename, "r") as f:
            mapping = json.loads(f.read())
    else:
        # Create image number to index mapping for mscoco images
        mapping = {}
        for idx, img in enumerate(glob.glob(folder_mscoco + "*")):
            mapping[img.split("_")[-1].split(".")[0]] = idx

        with open(complete_filename, "w") as f:
            json.dump(mapping, f)
    return mapping

def l1_smooth(matrix_a, matrix_b):
    return torch.mean(SMOOTH_L1(matrix_a, matrix_b), dim=1)


def get_most_similar(folder_mscoco, matrix_storage, mapping, net, device, distance_measure):
    # Constructs for cosine similarity and storing information
    top50 = {}
    if distance_measure == "cos":
        pdist = nn.CosineSimilarity(dim=1, eps=1e-6)
        sort_as = True
        print("Using cosine...")
    elif distance_measure == "l1":
        pdist = l1_smooth
        sort_as = False
        print("Using l1 smooth...")
    else:
        sort_as = False
        pdist = nn.PairwiseDistance(p=2)
        print("Using l2...")
    # Read in the visualSem data
    data_tensor = torch.Tensor().to(device)
    for n in range(1, AMOUNT_REP_FILES + 1):
        f = h5py.File(matrix_storage + BASE_NAME + str(n) + ".hdf5", "r")
        data = f.get("matrix_part").value
        data = torch.Tensor(data).to(device)
        data_tensor = torch.cat((data_tensor, data))

    print(data_tensor.size())

    for img, idx in tqdm(mapping.items(), mininterval=10):
        image = transform(Image.open(folder_mscoco + "COCO_train2014_" + img + ".jpg").convert("RGB")).unsqueeze(0).to(device)
        out = net(image)
        # Get cosine similarities
        cos_vals = pdist(data_tensor, out).cpu()
        vs, idxs = torch.sort(cos_vals, descending = sort_as)
        top50[idx] = (vs[:50].tolist(), idxs[:50].tolist())

    return top50

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--store_matrix", type = str, default = "data/matrix_reps/1000D/", help = "where representations are stored")
    parser.add_argument("--train_mscoco", type = str, default = "mscoco_data/data/train2014/", help = "where mscoco data is stored")
    parser.add_argument("--store_dicts", type = str, default = "data/matrix_reps/1000D_l1/", help = "where to store the dicts with top-n")
    parser.add_argument("--distance", type = str, default = "l1", help = "distance measure used, l2, l1 (smooth) or cos")
    parser.add_argument("--dim", type = int, default = 1000, help = "dimensionality of the matrix representations to use")
    args = parser.parse_args()
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(device)

    net = CNN(args.dim)
    net = net.to(device)
    print("Using a dimensionality of: " + str(args.dim))
    print("Check mapping for images mscoco...")
    mapping = map_mscoco_number(args.train_mscoco, args.store_dicts)
    print("Creating top-n information...")
    top50 = get_most_similar(args.train_mscoco, args.store_matrix, mapping, net, device, args.distance)

    with open(args.store_dicts + "top50.json", "w") as f:
        json.dump(top50, f)
