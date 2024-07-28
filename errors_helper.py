from functools import wraps

def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            # probably when argument is missing
            return "Error. Enter the argument for the command"
        except KeyError:
            # error accessing dict, probably wrong name 
            return "Error. Check you enter correct parameters."
        except IndexError:
            # FIXME?
            # Note that there is no obvious way to get IndexError in this code, but task demans it
            return "Index error. Make sure you enter command and parameters right."
        except:
            return "Unexpected error. Make sure you enter command and parameters right. Run \'info\' command if you have a quistion about how to use it"

    return inner