#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mi Master Camera Combo - Automated Module Verification Wrapper
Author: borndead
"""

import sys
from pathlib import Path

# Import core verification engine
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / 'tools'))

from verify import main

if __name__ == '__main__':
    main()
