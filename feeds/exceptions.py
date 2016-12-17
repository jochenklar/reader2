class FeedException(Exception):

    def __init__(self, *args, **kwargs):
        self.message = kwargs.pop('message')
