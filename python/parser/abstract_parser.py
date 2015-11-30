
class AbstractParser(object):
    """AbstractParser with standard filename methods, parse method has to be implemented by subclass"""
    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        """returns a list of talks, it is recommended to use the python generator for less memory usage"""
        raise NotImplementedError("to be implemented by subclass")

    def progress(self):
        """progress of parsing, should be implemented for parsers with large file sizes"""
        raise NotImplementedError("to be implemented by subclass")

    def _no_progress_function(self):
        return 0.

    def _line_count_progress(self):
        return float(self._progress) / self._linenumber

    def _init_line_count_progress(self):
        i = -1
        with open(self.filename) as f:
            for i, line in enumerate(f):
                pass
        self._linenumber = i + 1
        self._progress = 0

