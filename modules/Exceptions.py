class DirectionNotDetermined(BaseException):
    
    def __init__(self, message="Hand did not move in only one direction. Direction of movement cannot be determined."):
        self.message = message
        super().__init__(self.message)


