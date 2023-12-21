# a python package needs an __init__ file
# a package may have several modules (.py files)
from .reverser import Reverse
# importing the Reverse class from the reverser module
# it is like a shortcut for importing Reverse class directly
# the above line is needed otherwise
# one needs to import reverser everytime
# they need to use Reverse class
