
class BaseAgent:
    'Base class for agents'
    
    def __init__(self):
        pass
    
    
    # common api for children to implement
    
    def FetchItemInfoDetail(self):
        'Fetch & Fill-In "detail" parameter for supplied WebItemInfo.'
        raise NotImplementedError('Subclass must implement this method')
    
    def FetchParentChildren(self):
        'Fetch a Parent WebItemInfo\'s Children'
        raise NotImplementedError('Subclass must implement this method')
    
    def FetchUserInfo(self):
        'Fetch a WebItemInfo\'s UserInfo'
        raise NotImplementedError('Subclass must implement this method')
    
    def DownloadItem(self):
        'Download supplied WebItemInfo'
        raise NotImplementedError('Subclass must implement this method')
    
    
