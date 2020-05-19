def normal_comma(some_float):
    convertable = str(some_float)
    converted = ""
    for char in convertable:
        if char == ".":
            converted = converted + ","
        else:
            converted = converted + char
    return converted