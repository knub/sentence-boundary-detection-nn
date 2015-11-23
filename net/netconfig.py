import argparse

START_SYMBOL = '#### BLOCKSTART'
END_SYMBOL = '#### BLOCKEND'


def get_keyword(line):
    return line.split(" ")[-1].strip()

def main(prototxt, output, omissions, additions, verbose, print_to_stdout):
    try:
        input_file = open(prototxt)
    except IOError:
        print "IOError: Could not open '%s'!" % prototxt
        return
    lines = input_file.readlines()
    input_file.close()

    comment_change_level = 0
    for i in range(0, len(lines)):
        keyword = None
        if lines[i].startswith(START_SYMBOL):
            base_delta = 1
            keyword = get_keyword(lines[i])
        if lines[i].startswith(END_SYMBOL):
            base_delta = -1
            keyword = get_keyword(lines[i])
        final_delta = 0
        if keyword in omissions:
            final_delta = base_delta
        if keyword in additions:
            final_delta = base_delta * -1
        comment_change_level += final_delta
        if verbose and keyword: print ("keyword found: %s" % lines[i]),
        if keyword:
            # we do not want to change the keyword lines
            continue
        if comment_change_level > 0:
            lines[i] = '#' + lines[i]
            if verbose: print ("commented out: %s" % lines[i]),
        elif comment_change_level < 0:
            if (lines[i][0] == "#"):
                lines[i] = lines[i][1:]
                if verbose: print ("commented in:  %s" % lines[i]),
            else:
                print "warning: line %d (%s...) should be added, but does not start with a comment symbol!" % (i, lines[i][0:10])
        else:
            if verbose: print ("unchanged:     %s" % lines[i]),

    if print_to_stdout:
        for line in lines:
            print line,
        return 

    try:
        output_file = open(output,"w")
    except IOError:
        print "IOError: Could not open '%s'!" % prototxt
        return
    for line in lines:
        output_file.write(line)
    output_file.close()
    print "Modified net saved here: %s" % output

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Configure your net with #### BLOCKSTART and #### BLOCKEND tags')
    parser.add_argument('prototxt', help='the net prototxt you want to modify')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d','--deploy', help='preset: deploy (omit TRAINTEST blocks, add DEPLOY), default output is deploy.prototxt', action='store_true')
    group.add_argument('-f','--fulltest', help='preset: fulltest (omit TEST blocks, add FULLTEST), default output is fulltest.prototxt', action='store_true')
    parser.add_argument('-o','--output', help='output path of the modified net, default is taken from preset, or output.prototxt otherwise', default='output.prototxt', metavar='output')
    parser.add_argument('--omit', nargs='*', help='omit all blocks with these keywords (case-sensitive)', metavar='keyword', default=[])
    parser.add_argument('--add', nargs='*', help='add all blocks with these keywords (case-sensitive)', metavar='keyword', default=[])
    parser.add_argument('-v','--verbose', help='be verbose', action='store_true')
    parser.add_argument('-s','--stdout', help='print output to stdout instead of writing a file', action='store_true')
    args = parser.parse_args()

    # handle presets
    if (args.deploy):
        args.omit.append("TRAINTEST")
        args.add.append("DEPLOY")
        if args.output == "output.prototxt":
            args.output = "deploy.prototxt"
    if (args.fulltest):
        args.omit.append("TRAIN")
        args.add.append("FULLTEST")
        if args.output == "output.prototxt":
            args.output = "fulltest.prototxt"

    main(args.prototxt, args.output, args.omit, args.add, args.verbose, args.stdout)
