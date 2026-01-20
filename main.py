# Entrypoint for the program

# Library Imports


# Local Imports
from core.session import Session
from core.init import init
from repl.repl import REPL
from repl.exceptions import InvalidCommand, ParseError, MissingContext
from core.exceptions import NotImplementedError, ContextImplementationError



def main() -> None:
    """Main entrypoint for the program"""
    session = Session()
    init(session)

    while True:
        try:
            repl = REPL(session)
            repl.run()

        except InvalidCommand as e:
            session.io.warn(e)

        except ParseError as e:
            session.io.warn(e)

        except MissingContext as e:
            session.io.warn(e)

        except NotImplementedError as e:
            session.io.warn(e)

        except ContextImplementationError as e:
            session.io.warn(e)
            session.remove_active_head()


if __name__ == "__main__":
    main()