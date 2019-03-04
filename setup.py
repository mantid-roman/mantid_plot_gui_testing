from setuptools import setup, find_packages
import sys

# dependencies = ['six', 'pyyaml', 'markdown', 'click', 'numpy']

# if sys.version_info[0] == 2:
#     dependencies.append('pathlib2')

setup(
    name="mantid_plot_gui_testing",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    # install_requires=dependencies,
)

#  pip install -e git+git@bitbucket.org:roman_tolchenov/generate.git#egg=generate
