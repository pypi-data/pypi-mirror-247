# CodeePy

CodeePy has been created to allow Codee the robot from the Creative Science Foundation to be controlled via Python.
[![PyPI version](https://badge.fury.io/py/codeepy.svg)](https://badge.fury.io/py/codeepy)

# Getting started with CodeePy

## Requirements
CodeePy requires Python 3.4 or greater to be installed on your machine, it can be downloaded for free from the [Python website.](https://www.python.org/downloads/)
We recommend using [Pycharm IDE](https://www.jetbrains.com/pycharm/download/#section=windows) as your initial development tool, please note students, educators and educational facilities have free access to the professional version and there is also a free community version.

## Setting up your development environment
Create a new project, being sure to specify the Python 3.4 interpreter.
Open the terminal within PyCharm and install CodeePy with pip (which will also install any dependencies)
For more information regarding pip please visit our [module page](https://pypi.org/project/codeepy/)

```python
pip install codeepy
```

## Getting started
Within your project create a new Python file, initially you will need to import CodeePy, and create an instance of CodeePy.
I have included a helper which will list your com ports, additionally CodeePy documentation can be viewed with the help(CodeePy) function below

```python
from codeePy import CodeePy

# view CodeePy Documentation
help(CodeePy)

CodeePy.get_com_ports()

# create CodeePy Instance and open connection
codee = CodeePy('<Your COM port>')
```

Now you have created your instance object please see the Example.py file to test the CodeePy functions.


## Upgrading CodeePy

```python
pip install codeepy --upgrade
```


## About Codee & Creative-Robotix
Creative-Robotix can be used by teachers, parents, children, adults, in groups or as
individuals to address core STEAM (Science, Technology, Engineering, Arts & Maths) learning
and making activities in a fun, hands-on, social and interactive way. Our open-source
platform can be used by anyone from 7 years up who are interested in learning more about
technology. The tasks are carefully designed to fit the abilities of all ages, ranging from
simple to more complex assembly, depending on your age, knowledge and guidance
available

## Building Codee
For more information on how to create Codee including 3D printing files and firmware please visit [Instructables](https://www.instructables.com/id/Creative-Robotix-Educational-Platform-Codee-Robee-/)

For more information on the Creative Science Foundation please visit [CreativeRobotix](https://creative-science.org/partnerships/creative-robotix/)

				
