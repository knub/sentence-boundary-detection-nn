
class AbstractParser( object ):
    """AbstractParser which shows the interface and methods a parser should apply"""
    def parse(self):
        """returns a list of talks"""
        raise NotImplementedError("to be implemented by subclass")
