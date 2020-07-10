from PfsFile import PfsFile
import filecmp

""" 
This will load (parse) and then write back each of the given PFS files, and then compare the resulting files.
"""

import os
print(os.getcwd())

# MSHE main file
f = "./tests/MSHE_main.she"
she_file = PfsFile(f)
she_file.saveTo(f+".tmp")
print("{}: \t{}".format(f, filecmp.cmp(f, f+".tmp", shallow=False)))

# MSHE UZ property file
f = "./tests/MSHE_UzSoilProp.uzs"
she_file = PfsFile(f)
she_file.saveTo(f+".tmp")
print("{}: \t{}".format(f, filecmp.cmp(f, f+".tmp", shallow=False)))
