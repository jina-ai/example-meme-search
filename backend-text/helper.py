import os
import shutil
import sys
import json
from jina import Document, DocumentArray
from config import random_seed

def deal_with_workspace(dir_name, should_exist: bool = False, force_remove: bool = False):
    if should_exist:
        if not os.path.isdir(dir_name): # It should exist but it doesn't exist
            print(
                f"The directory {dir_name} does not exist. Please index first via `python app.py -t index`"
            )
            sys.exit(1)

    if not should_exist: # it shouldn't exist
        if os.path.isdir(dir_name):
            if not force_remove:
                print(
                    f"\n +----------------------------------------------------------------------------------+ \
                        \n |                                   🤖🤖🤖                                         | \
                        \n | The directory {dir_name} already exists. Please remove it before indexing again.  | \
                        \n |                                   🤖🤖🤖                                         | \
                        \n +----------------------------------------------------------------------------------+"
                )
                sys.exit(1)
            else:
                shutil.rmtree(dir_name)
