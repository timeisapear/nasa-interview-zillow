import os


def make_file_path(filename):
    return os.path.join(os.path.dirname(__file__), f"../data/{filename}")
