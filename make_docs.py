import pdoc
import os
import os.path as path
import re
from blaseball_mike.models.base import Base

output_dir = 'docs'


def recurse_modules(mod):
    yield mod
    for submod in mod.submodules():
        yield from recurse_modules(submod)


def recursive_write_files(m):
    filepath = path.join(output_dir, m.url())

    dirpath = path.dirname(filepath)
    if not os.access(dirpath, os.R_OK):
        os.makedirs(dirpath)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(m.html())

    for submodule in m.submodules():
        recursive_write_files(submodule)


# Generate documentation
mike_module = pdoc.Module('blaseball_mike')

# Dynamically pull fields for models and add them to the documentation
for module in recurse_modules(mike_module):
    for class_ in module.classes():
        if Base not in [x.obj for x in class_.mro()]:
            continue

        try:
            fields = class_.obj._get_fields()
        except AttributeError:
            continue

        for field in fields:
            if field in class_.doc:
                continue
            class_.doc[field] = pdoc.Variable(field, module, "", cls=class_, instance_var=True)

# Write to files
recursive_write_files(mike_module)
