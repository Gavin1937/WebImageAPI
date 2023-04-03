
from hashlib import md5
from typing import Union
from pathlib import Path
from io import BytesIO
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

def PPrintJson(json_obj:dict, indent:int=2):
    print(json.dumps(json_obj, indent=indent))

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
