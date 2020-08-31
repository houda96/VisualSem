from nltk import word_tokenize, pos_tag
from google_images_download import google_images_download
import json

OUT = 'data/babelnet_images'

if __name__ == "__main__":
    with open('data/nodes_1000.json', 'r') as f:
        nodes = json.loads(f.read())

    # Create sufficient descriptions for nodes without images in the core
    search_names = []
    zero_ims = [n for n in nodes if len(nodes[n]["images"]) == 0] # LINE TO CHANGE IF MORE NODES NEED IMAGES
    for n in zero_ims:
        sent = nodes[n]["description"][0]
        e = pos_tag(word_tokenize(sent))
        extra = [w[0] for w in e if "NN" in w[1] and (not w[0][0].isupper())]
        new_sent = nodes[n]["senses"][0].replace("_", " ").split() + extra
        search_names.append((" ".join(new_sent[:3]), n))

    print(search_names)

    response = google_images_download.googleimagesdownload()
    paths = []
    for (name, fold) in search_names:
        print("done")
        absolute_image_paths = response.download({"keywords":name,"limit":10,"print_urls":False,
                                                  "usage_rights":"labeled-for-reuse-with-modifications",
                                                  "output_directory":OUT, "image_directory":fold,
                                                 }) #"safe_search":True
        paths.append(absolute_image_paths)
