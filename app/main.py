import sys

from Gui import Gui
from Cli import Cli
from SDBridge import SDBridge


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "cli":
            cli = Cli()
            cli.monolog(sys.argv[2:])
        elif sys.argv[1] == "gui":
            ...
        else:
            raise BaseException("Karamba")
    else:
        #gui
        ...