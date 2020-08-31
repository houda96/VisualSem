import json
import urllib.request
import os

def get_key():
    with open("../data/key_babelnet.txt") as f:
        content = f.read()
    return content.replace('"', "").replace("\n", "")

def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)

def process_imgs(ims, folder_name):
    local_ims = []
    create_folder(folder_name)
    counts_all = 0
    counts_good = 0
    for url in ims:
        counts_all += 1
        filename = folder_name + "/" + url.split('/')[-1]
        print(filename)
        try:
            urllib.request.urlretrieve(url, filename)
            counts_good += 1
        except:
            continue
        local_ims.append(filename)
    return local_ims, counts_all, counts_good

def return_core_graph():
    dense_classes_file = "data/1000_classes.txt"
    with open(dense_classes_file) as f:
        content = f.read()

    rows_classes = content.split("\n")
    classes = [row.split()[0] for row in rows_classes]
    classes = ["wn:" + clas[1:] + clas[0] for clas in classes]
    return classes

def from_lemma_to_ids(lemma, key):
    # Requires key
    req_link = "https://babelnet.io/v5/getSynsetIds?lemma=" + lemma + "&searchLang=EN&key=" + key

    content = urllib.request.urlopen(req_link).read().decode('utf8').replace("'", '"')
    content = json.loads(content)
    return content

def from_synsetID_to_images(synset_id, key=None):
    if key:
        req_link = "https://babelnet.io/v5/getSynset?id=" + synset_id + "&key=" + key
        content = urllib.request.urlopen(req_link).read().decode('utf8').replace("'", '"')
    else:
        req_link = "http://10.0.0.100:8080/getSynset?id=" + synset_id
        content = urllib.request.urlopen(req_link).read().decode('utf8')

    content = json.loads(content)
    return content, content["images"]

def get_edges_from_synset(synset_id, key=None):
    if key:
        req_link = "https://babelnet.io/v5/getOutgoingEdges?id=" + synset_id + "&key=" + key
        content = urllib.request.urlopen(req_link).read().decode('utf8').replace("'", '"')
    else:
        req_link = "http://10.0.0.100:8080/getOutgoingEdges?id=" + synset_id
        content = urllib.request.urlopen(req_link).read().decode('utf8')

    content = json.loads(content)
    return content

def process_sense_info(id_syn, key=None):
    synset_info, synset_images = from_synsetID_to_images(id_syn, key)
    senses = list(set([entry["properties"]["fullLemma"] for entry in synset_info["senses"]]))
    glosses = list(set([entry["gloss"] for entry in synset_info["glosses"]]))
    main_sense = synset_info["mainSense"]
    ims = [img["url"] for img in synset_images]
    ims_bad = len([img for img in synset_images if img["badImage"]])
    synset_id = id_syn
    if "wn:" in id_syn:
        synset_id = list(set([sen["properties"]["synsetID"]["id"] for sen in synset_info["senses"]]))[0]
    return senses, glosses, main_sense, ims, synset_id, ims_bad

def edge_information(synset_id, key=None):
    edges_info = get_edges_from_synset(synset_id, key)
    edg_inf = [process_sense_info(edg["target"], key) + (edg["pointer"]["shortName"],
                    edg["pointer"]["name"], edg["weight"]) for edg in edges_info]
    edg_inf = [edg for edg in edg_inf ]
    possible_relations = list(set([edg[6] for edg in edg_inf]))
    relations = [Relation(synset_id, edg[4], edg[6], edg[7], edg[8]) for edg in edg_inf]
    next_order_nodes = [(edg[4], Node(edg[1], edg[3], 0, [], edg[0], edg[2])) for edg in edg_inf]
    return possible_relations, relations, len(edg_inf), next_order_nodes, [edg[5] for edg in edg_inf]
