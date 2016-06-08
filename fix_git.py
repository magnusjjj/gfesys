import os
import sys

os.system("git submodule update init --recursive")
os.system("git update-index --skip-worktree gfe/settings_local.py")