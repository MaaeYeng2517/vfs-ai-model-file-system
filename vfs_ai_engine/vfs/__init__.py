class VFSEngine:
    def __init__(self, root="/"):
        self.root = root
        self._files = {}
        self._dirs = {root}

    def mkdir(self, path, exist_ok=False):
        if path in self._dirs:
            if not exist_ok:
                raise FileExistsError(path)
            return
        parent = path.rsplit("/", 1)[0] or "/"
        if parent not in self._dirs:
            raise FileNotFoundError(parent)
        self._dirs.add(path)

    def write(self, path, content, namespace=None):
        parent = path.rsplit("/", 1)[0] or "/"
        if parent not in self._dirs:
            raise FileNotFoundError(parent)
        self._files[path] = {"content": content, "namespace": namespace}

    def read(self, path):
        if path not in self._files:
            raise FileNotFoundError(path)
        return self._files[path]["content"]

    def ls(self, path="/"):
        prefix = path.rstrip("/") + "/"
        return sorted({p[len(prefix):].split("/")[0] for p in list(self._files) + list(self._dirs) if p.startswith(prefix) and p != path})

    def delete(self, path):
        self._files.pop(path, None)
        self._dirs.discard(path)

    def exists(self, path):
        return path in self._files or path in self._dirs
