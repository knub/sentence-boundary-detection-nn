
class AbstractParser( object ):
    """AbstractParser which shows the interface and methods a parser should apply"""
    def parse(self):
        """returns a list of talks, it is recommended to use the python generator for less memory usage"""
        raise NotImplementedError("to be implemented by subclass")
