from .base import *

if DEBUG:
    from .dev import *
elif DOCKER:
    from .prod_docker import *
else:
    from .prod import *