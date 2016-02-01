import numpy, caffe

class AbstractClassifier(object):

    def _predict_batch(self, instances):
        if self.net.blobs['data'].count != len(instances):
            self.net.blobs['data'].reshape(len(instances), self.net.blobs['data'].channels, self.net.blobs['data'].height, self.net.blobs['data'].width)

        arrays = [numpy.expand_dims(i.get_array(), axis=0) for i in instances]
        for i in instances:
            concatenated_array = numpy.concatenate(arrays, 0)

        self.net.blobs['data'].data[...] = concatenated_array

        out = self.net.forward()
        return [a.reshape(a.shape[1:]) for a in numpy.split(out['softmax'], len(instances))]

    def _predict_caffe(self, instances, batchsize = 128):
        caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})

        batches = len(instances) / batchsize

        results = []

        for batch_index in range(0, batches):
            s = batch_index * batchsize
            e = (batch_index + 1) * batchsize
            results.extend(self._predict_batch(instances[s:e]))

        results.extend(self._predict_batch(instances[batches * batchsize:]))

        return results
