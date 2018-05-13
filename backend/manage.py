#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # prod will not use manage.py, dev only
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.development")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
