import os


# Will return path of '.extension' files splitted into toumor and normal lists of paths
class dirScanner:
    def __init__(self, path, extension):
        self._path = path
        self._extension = extension
        self._paths_normal = []
        self._paths_toumor = []

    def get_paths(self):
        print("Scanning for ." + self._extension + " files in : " + self._path)
        for root, dirs, files in os.walk(self._path):
            for file in files:
                if file.endswith("." + self._extension):
                    path = os.path.join(root, file)
                    if "normal" in path:
                        self._paths_normal.append(path)
                    else:
                        self._paths_toumor.append(path)

        return self._paths_normal, self._paths_toumor
