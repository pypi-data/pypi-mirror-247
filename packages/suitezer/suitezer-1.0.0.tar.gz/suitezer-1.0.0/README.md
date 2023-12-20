# Suitezer

Automate your Python code analysis packages!

## Features

Ever wanted to make another Python CLI program a plugin to yours? Now, you can!

Provide a list of Python CLI invocations along with their associated command line arguments in the `config.yaml` (or other `YAML`) file, and go to it!


## Installation and Setup

Suitezer can be installed like any package on PyPI, just use the command `pip install suitezer` in the location of your choice and you're ready to go!

Suitezer will require a file titled `config.yaml` to be present within the directory you want to run Suitezer on.  An example of how the `config.yaml` file should be set up is shown here:


Make sure that in the `arguments` secton of the config file you put the name of the file or directory you'd like to run Suitezer on.  If you are running Suitezer on a directory, be sure that the packages you include in the config file are able to run on a directory.  Any custom arguments you'd like to add into the execution of a package can also be included in the `arguments` section.

## Usage

Once you have your config file set, just type `suitezer` into your terminal and Suitezer will do the rest!  If you'd like to see the execution time of Suitezer just type `suitezer --timing` into your terminal and you'll see how long your suitezer run takes.
