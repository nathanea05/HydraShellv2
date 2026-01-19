# Entrypoint for the program

# Library Imports


# Local Imports
from core.session import Session
from repl.repl import REPL
from repl.exceptions import InvalidCommand, ParseError


def main() -> None:
    """Main entrypoint for the program"""
    session = Session()
    while True:
        try:
            repl = REPL(session)
            repl.run()

        except InvalidCommand as e:
            session.io.warn(e)

        except ParseError as e:
            session.io.warn(e)


if __name__ == "__main__":
    main()