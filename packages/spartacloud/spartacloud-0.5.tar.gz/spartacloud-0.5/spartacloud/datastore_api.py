import redis

class DataStore:

    def __init__(self, host='localhost', port=6381, password=None, db=0):
        '''
        
        '''
        self.host = host
        self.port = port
        self.db = db
        self.r = redis.StrictRedis(host=host, port=port, password=password, db=db)

    def get_keys(self) -> list:
        '''
        
        '''
        keys = self.r.keys('*')
        return [key.decode() for key in keys]
    
    def get_value(self, key):
        '''
        
        '''
        return self.r.get(key).decode()