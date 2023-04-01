
class BaseAgent:
    'Base class for agents'
    
    def __init__(self):
        pass
    
    
    # common api for children to implement
    
    def FetchItemInfoDetail(self):
        'Fetch & Fill-In "detail" parameter for supplied WebItemInfo.'
        raise NotImplementedError('Subclass must implement this method')
    
    def FetchParentChildren(self):
        'Fetch a Parent WebItemInfo\' Children'
        raise NotImplementedError('Subclass must implement this method')
    
    def FetchUserInfo(self):
        'Fetch a WebItemInfo\' UserInfo'
        raise NotImplementedError('Subclass must implement this method')
    
    def DownloadItem(self):
        'Download supplied WebItemInfo'
        raise NotImplementedError('Subclass must implement this method')
    
    
