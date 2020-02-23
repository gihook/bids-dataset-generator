import os


def get_bid_files(path):
    files = filter(lambda f: f.startswith("b"), os.listdir(path))
    image_paths = map(lambda x: os.path.join(path, x), files)

    return image_paths
