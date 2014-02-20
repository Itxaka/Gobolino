# -*- coding: utf-8 -*-
import sys

import main

sys.path.insert(0, '..')

main.app.run(main.app.config.get("HOST"))