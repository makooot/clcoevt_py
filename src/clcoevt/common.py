def str_to_bool(s):
    lower_s = s.lower()
    if lower_s in ["true", "t", "yes", "y", "on", "1"]:
        return True
    elif lower_s in ["false", "f", "no", "n", "off", "0"]:
        return False
    else:
        return not s==""
