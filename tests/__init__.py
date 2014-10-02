# import app

# import node_tests



# import os
# import inspect
# import re
# print __file__

# # files = os.listdir(__file__)
# # print files
# abspath = os.path.abspath(__file__)
# root = os.path.dirname(abspath)
# files = os.listdir(root)
# print root
# files.remove('__init__.py')
# names = map(lambda x: os.path.splitext(x)[0], files)
# # map(lambda x: __import__(x), names)
# print names
# modules = filter(lambda x: re.match('.*\.py$', x), files) 
# print modules
# print map(lambda x: __import__(os.path.join(root, x)), modules)

import seeds