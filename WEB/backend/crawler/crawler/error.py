class HTMLElementsNotFoundError(Exception):
    def __init__(self, location, cant_find_what):
        self.msg = "in " + location + "...HTMLElementsNotFoundError: " + "can't find " + cant_find_what

    def __str__(self):
        return self.msg
