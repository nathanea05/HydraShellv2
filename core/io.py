# Responsible for all input/output functions

# Library Imports
from dataclasses import dataclass, field
from logging import log
from pprint import pprint

# Local Imports
from repl.exceptions import CancelOperation


TERMINAL_WIDTH = 80
FILLER = "#"


@dataclass
class IO:
    """Class to manage all input/output functions"""


    ### INPUT ###

    def safe_input(self, prompt: str = "", required: bool = False, normalize: bool = False) -> str:
        """Safe input function. Allows user to quit the program at any time"""

        while True:
            response = input(prompt)
            normalized_response = response.strip().lower()
            if normalized_response == "cancel":
                raise CancelOperation("Operation cancelled by User")
            if required and not response:
                print("Invalid Input. Input is required")
                continue
            break
        if normalize:
            return normalized_response
        return response
            
    def confirm(self, prompt: str, default_no: bool = True) -> bool:
        """Prompts the user to confirm a prompt by entering y or n"""

        if default_no:
            suffix = "[y/N]"
        else:
            suffix = "[Y/n]"
        complete_prompt = f"{prompt.strip()} {suffix}: "

        while True:
            response = self.safe_input(prompt=complete_prompt, required=True, normalize=True)
            if response == "y":
                return True
            elif response == "n":
                return False
            else:
                print("Invalid Response. Must be either 'y' or 'n'.")
                continue


    ### OUTPUT ###

    def warn(self, message: str) -> None:
        """Prints a warning to the terminal"""
        print(f"[WARN] {message}")


    def _write_title(self, title: str):
        total_filler = TERMINAL_WIDTH - len(title)
        total_filler -= 2
        half_filler = (total_filler / 2)
        half_filler = int(half_filler)
        print(f"\n\n{FILLER * half_filler} {title} {FILLER * half_filler}\n")

    
    def _write_footer(self):
        print("\n")
        print(FILLER * TERMINAL_WIDTH)
        print("\n")


    def write(self, message: str = None, footer: bool = False) -> None:
        """Prints a message to the terminal"""
        if message:
            print(message)
        if footer:
            self._write_footer()


    def pwrite(self, message: str, title: str = None, footer: bool = False) -> None:
        """Prints a formatted message to the terminal (pprint)"""
        if title:
            self._write_title(title)

        pprint(message)

        if footer:
            self._write_footer()