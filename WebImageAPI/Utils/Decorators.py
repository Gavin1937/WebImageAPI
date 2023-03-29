

# multi-layer decorator
# decorator takes in parameters for itself
def TypeChecker(type_wanted, indexes:list):
    '''
    decorator for function parameter type checking
    Param:
        type_wanted => type wanted to match
        indexes     => iterable of indexes from original function arguments to check
    '''
    # 1st layer takes in original function
    def wrapper_top(func):
        # 2nd layer takes in parameters of original function
        def wrapper(*args, **kwargs):
            if not all(map(lambda i:type(args[i]) == type_wanted, indexes)):
                raise ValueError(f'Parameter must be a {type_wanted.__name__}')
            return func(*args, **kwargs)
        return wrapper
    return wrapper_top


def TypeMatcher(type_list:list):
    '''
    decorator for function parameter type matching
    all parameters must match "type_list"
    Param:
        type_list =>    list of types to match,
                        pass str 'self' as first element
                        if use it for a class function
    '''
    def wrapper_top(func):
        def wrapper(*args, **kwargs):
            tmp_args = args
            tmp_type_list = type_list
            if tmp_type_list[0] == 'self':
                tmp_type_list = type_list[1:]
                tmp_args = args[1:]
            if not all(map(lambda i:type(i[0]) == i[1], zip(tmp_args, tmp_type_list))):
                raise ValueError(f'Parameters not matching: {type_list}')
            return func(*args, **kwargs)
        return wrapper
    return wrapper_top
