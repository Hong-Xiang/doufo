from pkg_resources import get_distribution
__version__ = get_distribution('doufo').version
from .control import *
from .monoid import Monoid
from .function import *
from .list import *
from .iterable import *
from .maybe import Maybe
from .on_collections import *
from .pair import Pair
from ._dataclass import *
from .qlambda import *