class ACCError(Exception):
    def __init__(self, acc: str):            
        # Call the base class constructor with the parameters it needs
        super().__init__(f"I cannot process acc: {acc}")
            
        # Now for your custom code...
        self.acc = acc