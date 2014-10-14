# import app

# import node_tests



# import os
# import inspect
# import re

# # files = os.listdir(__file__)
# abspath = os.path.abspath(__file__)
# root = os.path.dirname(abspath)
# files = os.listdir(root)
# files.remove('__init__.py')
# names = map(lambda x: os.path.splitext(x)[0], files)
# # map(lambda x: __import__(x), names)
# modules = filter(lambda x: re.match('.*\.py$', x), files) 
# print map(lambda x: __import__(os.path.join(root, x)), modules)
