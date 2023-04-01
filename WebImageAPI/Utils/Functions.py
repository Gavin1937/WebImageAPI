
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
