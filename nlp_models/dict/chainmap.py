import builtins
pylookup = ChainMap(locals(), globals(), vars(builtins))

print(__builtins__)

