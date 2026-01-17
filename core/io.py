# Responsible for all input/output functions

# Library Imports
from dataclasses import dataclass, field
from logging import log

# Local Imports
from core.exceptions import CancelOperation


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
            if normalized_response == "quit":
                print("Goodbye!")
                quit()
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