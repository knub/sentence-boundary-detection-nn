import leveldb, argparse, numpy
from caffe.proto import caffe_pb2


class CreateLevelDB():
    """create a new level db, fill it with word vectors"""
    def __init__(self, filename, batchsize = 1000):
        self.__filename = filename
        self.__db = leveldb.LevelDB(filename)
        self.__current_batch_size = 0
        self.__batch = None
        self.__index = 0
        self.batchsize = batchsize

    def writeTrainingInstance(self, vectors, label):
        if (self.__batch == None):
            self.__batch = leveldb.WriteBatch()

        datum = caffe_pb2.Datum()
        datum.channels, datum.height, datum.width = vectors.shape        
        # datum.channels = 1
        # datum.height = len(vectors)
        # datum.width = len(vectors[0])
        datum.label = label
        datum.float_data.extend(vectors.flat)

        self.__batch.Put(str(self.__index), datum.SerializeToString())

        self.__index += 1
        self.__current_batch_size += 1

        if (self.__current_batch_size == self.batchsize):
            self.__db.Write(self.__batch, sync = True)
            self.__batch = None
            self.__current_batch_size = 0

    def close(self):
        if (self.__batch):
            self.__db.Write(self.__batch, sync = True)
            self.__batch = None
        self.__current_batch_size = 0
        self.__db = None

    def read(self, key):
        return self.__db.Get(key)

def main(args):
    # write
    ldbCreation = CreateLevelDB(args.dbfile)

    channels = 1
    window_size = 5
    vector_size = 300
    dimensions = (channels, window_size, vector_size)

    for i in range(0, 1000):
        sample = numpy.zeros(dimensions)
        label = i

        # fill with vector data
        for x in range (dimensions[0]):
            for y in range (dimensions[1]):
                for z in range (dimensions[2]):
                    sample[x,y,z] = x * 1000 + y * 100 + z
        ldbCreation.writeTrainingInstance(sample, label)
    # close after you are done!
    ldbCreation.close()

    # # read
    # ldbCreation = CreateLevelDB(args.dbfile)
    # datum = caffe_pb2.Datum()
    # datum.ParseFromString(ldbCreation.read("50"))
    # print datum
    # print datum.label

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Write a test file.')
    parser.add_argument('dbfile', help='path to a level db test directory')
    args = parser.parse_args()
    main(args)
