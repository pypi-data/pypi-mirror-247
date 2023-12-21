<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="static/logo/icon.jpg" alt="Project logo"></a>
</p>

<h3 align="center">Kami Messenger</h3>

<div align="center">

[![GitHub release](https://img.shields.io/github/release/devkami/kami-messenger.svg)](https://GitHub.com/devkami/kami-messenger/releases/)
[![GitHub issues](https://badgen.net/github/issues/devkami/kami-messenger/)](https://github.com/devkami/kami-messenger/issues/)
[![License](https://img.shields.io/badge/License-GNU-blue)](/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/kami-messenger/badge/?version=latest)](https://kami-messenger.readthedocs.io/en/latest/?badge=latest)
![CI](https://github.com/devkami/kami-messenger/actions/workflows/pipeline.yml/badge.svg)

</div>

---

<p align="center"> Aggregator of Digital Channels For Sending Messages
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [TODO](../TODO.md)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

Kami Messenger is a tool for aggregating several messaging platforms into a single package in order to facilitate the task of sending mass messages.

It contains three main classes for this purpose:

- Message(A single message that contains a list of recipients to send);
- Contact(A single contact with a list of addresses for different messaging platforms);
- Messenger(An object that instantiates, connects, and provides message push service of a specific platform)

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

To run this package you only need a [python 3.x](https://www.python.org/downloads/) compiler and [poetry](https://python-poetry.org/) on your dev enviroment.


### Installing

```bash
pip install kami-messenger
```

Then, after installing the dependencies, just activate the development environment with the following command:

```bash
poetry shell
```

Ready now you start developing and testing!

## 🔧 Running the tests <a name = "tests"></a>

The project already has some of the main unit tests for each of the entities present in the code, but you can add your own tests in the respective directories 'test' of each entity.

### Break down into end to end tests

Each entity has its own tests folder with the most elementary unit tests and to run them just run the command below in the entity folder you want to test or in the root folder to test all project codes

```terminal
task test
```

>Note that when executing this command, before actually testing the code, a code review will be performed using the lint-review task and after the execution of the test, an html file with the full coverage of the test will be available in the htmlcov folder created in the folder where the command was run. was executed

### And coding style tests

In addition, the project already has automated tasks for review and correcting the code style following pep8 standards

To just review the code run the command below in the folder you want to analyze:

```terminal
task lint-review
```

If you want to automatically review and correct the code, run this command in the desired directory

```terminal
task lint-fix
```

## 🎈 Usage <a name="usage"></a>

Add notes about how to use the system.

## 🚀 Deployment <a name = "deployment"></a>

Add additional notes about how to deploy this on a live system.

## ⛏️ Built Using <a name = "built_using"></a>

- [Python 3.x](https://www.python.org/downloads/)
- [Python email built-in lib](https://docs.python.org/3/library/email.examples.html)

## ✍️ Authors <a name = "authors"></a>

- [@maicondmenezes](https://github.com/maicondmenezes) - Idea & Initial work


See also the list of [contributors](https://github.com/devkami/kami_messenger/contributors) who participated in this project.

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- The main references for this project can be found in the Python topic of [this repository](https://github.com/devkami/kami_wiki/blob/main/python_estudies.md)
