from .colors import Bcolors

def print_message(title: str, message: str = "", color=0):
    start = ''
    print(f'{start}===================={title}===================={Bcolors.ENDC}')
    print(f'{start}{message}{Bcolors.ENDC}')

def print_debug(message: str):
    print(f'{Bcolors.OKGREEN}{message}{Bcolors.ENDC}')