from ..utils.colors import Bcolors

class SQLError(Exception):
    def __init__(self, line: int, cause: str, statement: str):            
        # Call the base class constructor with the parameters it needs
        super().__init__(f"SQL error in line {line}: {statement}")
            
        # Now for your custom code...
        self.line = line
        self.cause = cause
        self.statement = statement

    def to_json(self) -> dict:
        return {
            "cause" : self.cause,
            "statement" : self.statement
        }

    def __str__(self) -> str:
        return f'SQL error in line {self.line}: {self.statement} \n {Bcolors.OKGREEN} err: {self.cause} {Bcolors.ENDC}'