import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import glob, os
import argparse
from tqdm import tqdm
import json
from cnn import CNN
import h5py

normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
transform = transforms.Compose([transforms.RandomResizedCrop(224), transforms.RandomHorizontalFlip(),
                transforms.ToTensor(), normalize])

def prepare_data(node_file):
    with open(node_file, 'r') as f:
        nodes = json.loads(f.read())

    mapping_ims = {n:v['ims'] for n, v in nodes.items()}

    return mapping_ims

def load_image(file_name, file_folder, transform = None):
    path = file_folder + file_name[:2] + "/" + file_name + ".jpg"
    try:
        image = Image.open(path).convert("RGB")
    except FileNotFoundError:
        image = Image.open(path[:-4]).convert("RGB")
    except IOError:
        image = Image.open(path)

    if transform:
        image = transform(image)

    return image

def calculate_and_store_repres(net, mapping_ims, images_folder, matrix_storage, batch_size, device):
    stored_reps = torch.Tensor()
    num = 1
    for idx, node in tqdm(enumerate(sorted(mapping_ims.keys())), mininterval = 10):
        ims = mapping_ims[node]
        cur = torch.Tensor()
        batches = [ims[i:i + batch_size] for i in range(0, len(ims), batch_size)]
        # Batch images and combine
        for batch in batches:
            input = torch.stack(tuple([load_image(im, images_folder, transform) for im in batch])).to(device)
            out = net(input)
            cur = torch.cat((cur, out.cpu()))

        stored_reps = torch.cat((stored_reps, torch.mean(cur, dim=0).unsqueeze(dim=0)))

        # Write back to file
        if ((idx + 1) % 10000) == 0:
            with h5py.File(matrix_storage + "matrix_representations" + str(num) + ".hdf5", "w") as f:
                dset = f.create_dataset("matrix_part", data=stored_reps)
            stored_reps = torch.Tensor()
            num += 1

    # Remaining information stored 
    with h5py.File(matrix_storage + "matrix_representations" + str(num) + ".hdf5", "w") as f:
        dset = f.create_dataset("matrix_part", data=stored_reps)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type = int, default = 30, help = "batch size of forward call, default=30")
    parser.add_argument("--nodes_file", type = str, default = "nodes_new.json", help = "where nodes are stored")
    parser.add_argument("--images_folder", type = str, default = "visualsem/", help = "where images are stored")
    parser.add_argument("--store_matrix", type = str, default = "visualsem/matrix_reps/1000D/", help = "where to store representations")
    parser.add_argument("--dim", type = int, default = 2048, help = "dimensionality of the cnn, 1000 or 2048")
    args = parser.parse_args()
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(device)

    net = CNN(args.dim)
    net = net.to(device)
    print("Prepare data...")
    mapping_ims = prepare_data(args.nodes_file)
    print("Obtain the representations...")
    calculate_and_store_repres(net, mapping_ims, args.images_folder, args.store_matrix, args.batch, device)
    print("Done")
