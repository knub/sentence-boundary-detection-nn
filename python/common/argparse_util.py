def is_valid_file(parser, arg, mode='r'):
    try:
        f = open(arg, mode)
        f.close()
        return arg
    except IOError:
        parser.error('The file %s can not be opened!' % arg)
