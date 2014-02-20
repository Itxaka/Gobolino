# -*- coding: utf-8 -*-
import sys

from web import main

sys.path.insert(0, '..')

main.app.run(main.app.config.get("HOST"))