class PandasStub:
    def __getattr__(self, attr):
        raise LibraryNotInstalledError("pandas")


class LibraryNotInstalledError(Exception):
    def __init__(self, library_name):
        self.library_name = library_name
        self.message = f"{library_name} is not installed. Please install it using 'pip install {library_name}'."
