"""

File: inspy_logger/__about__.py
Project: inSPy-Logger
Description:
    Holds information about the inSPy-Logger program and its version.

Created: 11/3/22 - 21:05:06

Since:
    v2.1.1

"""
from inspy_logger.version import parse_version

__prog__ = 'inSPy-Logger'
__version__ = parse_version()
__authors__ = [
        ('Inspyre-Softworks', 'https://inspyre.tech'),
        ('Taylor-Jayde Blackstone', '<t.blackstone@inspyre.tech')
]

'''
File Change History:
11/5/22 - 4:21 AM (v2.1.2):
  -  Added description to docstring. (target: 2.1.2)
 
11/5/22 - 4:41 AM:
  - Version bump (target: 2.1.3)
  
08/16/2023 - 13:49 (v3.0):
  - Version bump (v2.1.3 -> v3.0-dev.1)

'''
