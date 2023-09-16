import os
import shutil
from distutils.command.build_ext import build_ext
from distutils.core import Distribution, Extension

from Cython.Build import cythonize



def build():
    extensions = [
    ]
    ext_modules = cythonize(
        extensions,
        annotate=True,
        compiler_directives={'language_level': "3str"}
    )

    distribution = Distribution({"name": "extended", "ext_modules": ext_modules})
    distribution.package_dir = "extended"

    cmd = build_ext(distribution)
    cmd.ensure_finalized()
    cmd.run()

    # Copy built extensions back to the project
    for output in cmd.get_outputs():
        relative_extension = os.path.relpath(output, cmd.build_lib)
        shutil.copyfile(output, relative_extension)
        mode = os.stat(relative_extension).st_mode
        mode |= (mode & 0o444) >> 2
        os.chmod(relative_extension, mode)


if __name__ == "__main__":
    build()