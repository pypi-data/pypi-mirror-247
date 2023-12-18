from setuptools import setup

name = "types-pyinstaller"
description = "Typing stubs for pyinstaller"
long_description = '''
## Typing stubs for pyinstaller

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`pyinstaller`](https://github.com/pyinstaller/pyinstaller) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`pyinstaller`.

This version of `types-pyinstaller` aims to provide accurate annotations
for `pyinstaller==6.3.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/pyinstaller. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `d3bf2805b46b61ea9c08d07efbfac5a4f0b9ae73` and was tested
with mypy 1.7.1, pyright 1.1.339, and
pytype 2023.12.8.
'''.lstrip()

setup(name=name,
      version="6.3.0.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pyinstaller.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-setuptools'],
      packages=['pyi_splash-stubs', 'PyInstaller-stubs'],
      package_data={'pyi_splash-stubs': ['__init__.pyi', 'METADATA.toml'], 'PyInstaller-stubs': ['__init__.pyi', '__main__.pyi', 'building/__init__.pyi', 'building/api.pyi', 'building/build_main.pyi', 'building/datastruct.pyi', 'building/splash.pyi', 'compat.pyi', 'depend/__init__.pyi', 'depend/analysis.pyi', 'depend/imphookapi.pyi', 'isolated/__init__.pyi', 'isolated/_parent.pyi', 'lib/__init__.pyi', 'lib/modulegraph/__init__.pyi', 'lib/modulegraph/modulegraph.pyi', 'utils/__init__.pyi', 'utils/hooks/__init__.pyi', 'utils/hooks/conda.pyi', 'utils/win32/versioninfo.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
