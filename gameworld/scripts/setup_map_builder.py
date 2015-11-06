"""
Setup script for running map builder scripts
"""

import os, sys

# Since we aren't in the project root, add that to the path so we can find gamesite.setings
sys.path.append('../..')

# Set the Django Settings module environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gamesite.settings")

# Setup Django so we can use all modules and DB
import django
django.setup()
