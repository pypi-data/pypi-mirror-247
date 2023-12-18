import pathlib
from setuptools import setup, find_packages
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="marlware",  #todo:20230824修改 "rware" 为 "marlware"
    version="1.0.4",
    description="Multi-Robot Warehouse environment for reinforcement learning",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Filippos Christianos",
    url="https://github.com/semitable/robotic-warehouse",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),   #todo:20231211如果打包或者调用不成功，这里要试着修改一下
    classifiers=[
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",#todo:20231212修改“3.7”为“3.8”
    ],
    install_requires=[
        "numpy",
        "gym==0.21", #todo:20231212修改“0.21”为“0.18”
        "pyglet",
        "networkx",
    ],
    extras_require={"test": ["pytest"]},
    include_package_data=True,
)
