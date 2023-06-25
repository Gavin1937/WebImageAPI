
from hashlib import md5
from typing import Union
from pathlib import Path
from io import BytesIO
import operator as op
import json


# helper functions

def Clamp(val, bottom=None, top=None):
    'Clamp "val" in between "bottom" & "top" (optional & include both end)'
    if bottom is not None and val <= bottom:
        return bottom
    elif top is not None and val >= top:
        return top
    return val

def MergeDeDuplicate(iterable_1, *args) -> list:
    return list(set([*iterable_1, *[a for arg in args for a in arg]]))

def PPrintJson(json_obj:dict, indent:int=2, ensure_ascii:bool=False):
    print(json.dumps(json_obj, indent=indent, ensure_ascii=ensure_ascii))

def GetMD5(file:Union[str,Path,bytes,BytesIO]):
    output = None
    if isinstance(file, str) or isinstance(file, Path):
        file = Path(file)
        with open(file, 'rb') as fp:
            output = md5(fp.read()).hexdigest()
    elif isinstance(file, bytes):
        output = md5(file).hexdigest()
    elif isinstance(file, BytesIO):
        output = md5(file.read()).hexdigest()
    
    return output

def mkCompFunc(operator:str, param1=None):
    '''
    Create a comparison function with operator
    Param:
        operator     => str operator, can be: <, >, <=, >=, =, ==, !=
        param1       => left parameter for the function, can be None
                        if have param1, output function will take 1 parameter comparing with param1
                        else, output function will take 2 parameters
    Return:
        A comparison function with 1 or 2 parameter
    '''
    opfunc = None
    if operator == '<':
        opfunc = op.lt
    elif operator == '<=':
        opfunc = op.le
    elif operator == '>':
        opfunc = op.gt
    elif operator == '>=':
        opfunc = op.ge
    elif operator == '=' or operator == '==':
        opfunc = op.eq
    elif operator == '!=':
        opfunc = op.ne
    else:
        raise ValueError('Invalid operator. It must be <, >, <=, >=, =, ==, !=')
    
    if param1 is None:
        return (lambda p1,p2: opfunc(p1, p2))
    else:
        return (lambda p1: opfunc(param1, p1))

def mkCompFuncR(operator:str, param1=None):
    '''
    Same as mkCompFunc, but param1 is a right parameter
    Param:
        operator     => str operator, can be: <, >, <=, >=, =, ==, !=
        param1       => right parameter for the function, can be None
                        if have param1, output function will take 1 parameter comparing with param1
                        else, output function will take 2 parameters
    Return:
        A comparison function with 1 or 2 parameter
    '''
    opfunc = None
    if operator == '<':
        opfunc = op.lt
    elif operator == '<=':
        opfunc = op.le
    elif operator == '>':
        opfunc = op.gt
    elif operator == '>=':
        opfunc = op.ge
    elif operator == '=' or operator == '==':
        opfunc = op.eq
    elif operator == '!=':
        opfunc = op.ne
    else:
        raise ValueError('Invalid operator. It must be <, >, <=, >=, =, ==, !=')
    
    if param1 is None:
        return (lambda p1,p2: opfunc(p1, p2))
    else:
        return (lambda p1: opfunc(p1, param1))
