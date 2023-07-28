import os

ENV = os.environ.get("DJANGO_ENV")

if ENV == "production":
    from .settings_dep import *
else:
    from .settings_dev import *