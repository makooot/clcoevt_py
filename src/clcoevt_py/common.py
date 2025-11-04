class C:
    pass


def str_to_bool(s):
    if s == "true":
        return True
    elif s == "false":
        return False
    else:
        raise ValueError("Invalid boolean string")
