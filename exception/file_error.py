class FileError(Exception):
    def __init__(self, key: str, path: str):            
        # Call the base class constructor with the parameters it needs
        super().__init__(f"trying to read {key} on the path: {path}")
            
        # Now for your custom code...
        self.key = key
        self.path = path