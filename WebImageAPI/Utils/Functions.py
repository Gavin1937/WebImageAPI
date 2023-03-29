
# helper functions

def Clamp(val, bottom=None, top=None):
    'Clamp "val" in between "bottom" & "top" (optional & include both end)'
    if bottom is not None and val <= bottom:
        return bottom
    elif top is not None and val >= top:
        return top
    return val


