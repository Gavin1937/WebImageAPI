
# ################################################################## #
#                                                                    #
# A simple Singleton decorator for api agents in WebImageAPI         #
#                                                                    #
# Author: Gavin1937                                                  #
# GitHub: https://github.com/Gavin1937/WebImageAPI                   #
#                                                                    #
# ################################################################## #

from threading import Lock


# source 1: https://stackoverflow.com/questions/31875/is-there-a-simple-elegant-way-to-define-singletons
# source 2: https://medium.com/analytics-vidhya/how-to-create-a-thread-safe-singleton-class-in-python-822e1170a7f6
class Singleton:
    """
    A thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.
    
    The decorated class can define one `__init__` function that
    takes only the `self` argument. Also, the decorated class cannot be
    inherited from. Other than that, there are no restrictions that apply
    to the decorated class.
    
    To get the singleton instance, use the `instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.
    """
    
    def __init__(self, decorated):
        # set decorated class
        self._decorated = decorated
        self._instance = None
        self._lock = Lock()
    
    def instance(self, *args, **kwargs):
        """
        Returns the singleton instance.
        Upon its first call, it creates a new instance of the decorated class
        and calls its `__init__` method with supplied `args`.
        On all subsequent calls, the already created instance is returned.
        """
        if self._instance is None:
            with self._lock:
                # check again in case another thread acquired the lock before current one
                if self._instance is None:
                    self._instance = self._decorated(*args, **kwargs)
        return self._instance
    
    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')
    
    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)

