

class UserInfo:
    'User Information'
    
    def __init__(self, name_list:list, url_dict:dict, details:dict=dict()):
        self.name_list:list = name_list
        self.url_dict:dict = url_dict
        self.details:dict = details
    
    def __repr__(self):
        return f'<name_list={self.name_list}, url_dict={self.url_dict}>'
    
    def __str__(self):
        return f'<name_list={self.name_list}, url_dict={self.url_dict}>'
    
