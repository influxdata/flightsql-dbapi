from flightsql.exceptions import Error


def check_closed(f):
    def g(self, *args, **kwargs):
        if self.closed:
            raise Error(f"{self.__class__.__name__} already closed")
        return f(self, *args, **kwargs)

    return g
