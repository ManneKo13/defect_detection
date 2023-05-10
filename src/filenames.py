import os
import glob

class Filenames():
    def __init__(self, cwd: str) -> None:

        # List of filenames in directory points
        self.fn_area = [os.path.basename(x) for x in glob.glob(cwd + '/data/area/*.png')]
        # List of filenames in directory points
        self.fn_ok = [os.path.basename(x) for x in glob.glob(cwd + '/data/ok/*.png')]
        # List of filenames in directory points
        self.fn_pattern = [os.path.basename(x) for x in glob.glob(cwd + '/data/points/*.png')]
        # List of filenames in directory points
        self.fn_points = [os.path.basename(x) for x in glob.glob(cwd + '/data/points/*.png')]
    