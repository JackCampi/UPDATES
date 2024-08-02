class EquivalenceError(Exception):
    def __init__(self, name: str, not_found: str):            
        # Call the base class constructor with the parameters it needs
        super().__init__(f"No {name} registered: {not_found}")
            
        # Now for your custom code...
        self.name = name
        self.not_found = not_found