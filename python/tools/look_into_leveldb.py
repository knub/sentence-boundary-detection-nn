import leveldb, argparse
from caffe.proto import caffe_pb2


def main(leveldb_dir, limit):
    datum = caffe_pb2.Datum()
    db = leveldb.LevelDB(leveldb_dir)
    for i in range (0, limit):
        datum.ParseFromString(db.Get(str(i)))
        print datum.float_data, datum.label

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Print (beginning of) contents of a level db database.')
    parser.add_argument('leveldb', help='path to level db folder')
    parser.add_argument('-l','--limit', help='number of entries which should be displayed', type=int, default=10)
    args = parser.parse_args()
    main(args.leveldb, args.limit)
