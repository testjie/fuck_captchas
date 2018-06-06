﻿# -*- coding: utf-8 -*-
__author__ = 'snake'

from app import create_app
from app.api import rc, scmcc

app = create_app("ProductionConfig")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81, threaded=True)
