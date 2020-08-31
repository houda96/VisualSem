import json
import glob
from tqdm import tqdm
from PIL import Image


if __name__ == "__main__":
    good_examples = []
    bad_examples = []
    files = [j for i in glob.glob("../../../../images/new/*") for j in glob.glob(i + "/*")]
    for file in tqdm(files, mininterval=10):
        try:
            im = Image.open(file)
            good_examples.append(file)
        except:
            bad_examples.append(file)

    print(len(good_examples))
    print(len(bad_examples))
    print(len(good_examples)/(len(good_examples) + len(bad_examples))*100)

    with open("good_examples.json", "w") as f:
        json.dump(good_examples, f)

    with open("bad_examples.json", "w") as f:
        json.dump(bad_examples, f)
