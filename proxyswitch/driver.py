class Driver:
    '''
        Holds the driver state so the flasked script can change behaviour based
        on what the user injects via HTTP
    '''
    name = 'nobody'

    def start(self, name):
        self.name = name
        return self.name

    def stop(self):
        self.name = 'nobody'
        return self.name

