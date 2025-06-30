from importlib import reload
import core

reload(core)
from core import *

if __name__ == "__main__":
    main_header()
    main()