import os

# Text search
TEXT_PORT = 45679
TEXT_SERVER = os.getenv("BACKEND_TEXT", "0.0.0.0")
TEXT_SAMPLES = ["cute fuzzy animals", "so you're telling me willy wonka", "school sucks"]

# Image search
IMAGE_SERVER = os.getenv("BACKEND_IMAGE", "0.0.0.0")
IMAGE_PORT = 65432

# General
TOP_K = 10
DEBUG = os.getenv("DEBUG", False)
DATA_DIR = "../data"

