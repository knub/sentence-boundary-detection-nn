import argparse


def main():
	pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get word vector from binary data.')
    parser.add_argument('--datafile', help='path to file with text, if not present text can be entered interactively')
    parser.add_argument('vectorfile', help='path to word vector binary')
    parser.add_argument('caffemodel', help='path to caffe model file')
    parser.add_argument('caffeproto', help='path to caffe proto file')
    args = parser.parse_args()
    main(args)
