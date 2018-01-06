import os
import sys

from core.application import Application

os._exit(Application(sys.argv).run())
