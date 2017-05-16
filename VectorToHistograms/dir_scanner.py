import os
class dirScanner:

    def __init__(self, path, extension):
        self._path = path
        self._extension = extension
        self._paths = []
        self.get_paths()

    def get_paths(self):
        print("Scanning for " + self._extension + " files in : " + self._path)
        for root, dirs, files in os.walk(self._path):
            for file in files:
                if file.endswith("." + self._extension):
                    self._paths.append(os.path.join(root, file))

        print (self._paths)