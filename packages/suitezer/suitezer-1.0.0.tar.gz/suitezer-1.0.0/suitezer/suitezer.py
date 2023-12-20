import sys
import yaml
import pkg_resources
from arglite import parser as cliarg
import time
import subprocess

TIMING = (cliarg.optional.timing)

class Suitezer:

    @staticmethod
    def reset_args() -> None:
        """ Resets command-line arguments from prior binaries """
        values = len(sys.argv) - 1
        while len(sys.argv) > 0:
            del sys.argv[values]
            values -= 1
        sys.argv.append("")

    @staticmethod
    def load_config(filename: str = "config.yaml") -> dict:
        """ Loads the configuration file """
        with open("config.yaml", "r") as fh:
            config = yaml.safe_load(fh)
        return config

    @staticmethod
    def discover_modules(modules: list = [], mod_group: str = "console_scripts") -> list[pkg_resources.EntryPoint]:
        """ Discovers entry points for system modules """
        # Provides a list of all modules with entry points
        pkgs = pkg_resources.iter_entry_points(group = mod_group)

        # Returns a list of the module entry point accompanied by args from config.yaml
        return [(pkg, modules[pkg.name]["args"]) for pkg in pkgs if pkg.name in modules]

    @staticmethod
    def install_packages(modules: list = []):
        """ Installs the apropriate packages from Pypi """

        for module in modules:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', module])

    @staticmethod
    def run_module(entry_point: pkg_resources.EntryPoint, arguments: list = []) -> None:
        """ Runs module based on reported entry point """   
        # Apply any arguments provided in config
        for arg in arguments:
            if arg is not None:
                sys.argv.append(arg)
        # Load the entry point (removes need for importlib)
        entry = entry_point.load()
        # Run the program entry point
        try:
            entry()
        # If a package ends in a System exit, bypass
        except SystemExit:
            pass

def main():
    """ Main function """
    suite = Suitezer()
    config = suite.load_config()
    # Install the required dependencies
    suite.install_packages(modules = config["modules"])
    # Supply relevant modules to filter the list
    entry_points = suite.discover_modules(modules = config["modules"])
    for entry in entry_points:
        print(entry[0])
    # For each discovered module, run the process
    suite.reset_args()
    if TIMING:
        time0 = time.time()
    for entry in entry_points:
        # Run the module by providing the module entry and the args
        print(f"running", entry[0].name)
        suite.run_module(entry_point = entry[0], arguments = entry[1])
        # Blast the previously-supplied args

        suite.reset_args()
    if TIMING:
        time1 = time.time()
        print("execution time:", time1 - time0)

if __name__ == "__main__":
    main()
