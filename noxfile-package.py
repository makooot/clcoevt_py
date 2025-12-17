import sys
import os
import nox
from nox_uv import session

nox.options.default_venv_backend = "uv"

@session(python=["3.14"])
def tests(s: nox.Session) -> None:
    """session for testing the package"""

    # remove src from sys.path to ensure testing the installed package
    src_dir = os.path.join(os.path.dirname(__file__), "src")
    if src_dir in sys.path:
        sys.path.remove(src_dir)
    s.debug(f"sys.path: {sys.path}")

    # install the package
    s.install("--no-index", "--find-links=./dist", "clcoevt")

    # run the tests
    s.run("python", "-m", "unittest", "discover", "-s", "test_package")
