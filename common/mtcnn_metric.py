
import mxnet as mx
import numpy as np


class MtcnnAcc(mx.metric.EvalMetric):
    def __init__(self, name='acc', output_names=('mtcnn_prob',), label_names=('prob_label',)):
        super(MtcnnAcc, self).__init__(name, output_names=output_names, label_names=label_names)

    def update(self, labels, preds):
        assert len(preds) == 1
        assert len(labels) == 1

        prob = preds[0]
        prob_label = labels[0]

        pred_label = mx.nd.argmax(prob, axis=1).asnumpy().astype('int32')
        label = prob_label.asnumpy().astype('int32')
        mask = prob_label.asnumpy().astype('int32') >= 0

        self.sum_metric += ((pred_label == label) * mask).sum()
        self.num_inst += mask.sum()


class MtcnnClsRatio(mx.metric.EvalMetric):
    def __init__(self, cls, name='cls_ratio', output_names=('mtcnn_prob',), label_names=('prob_label',)):
        super(MtcnnClsRatio, self).__init__(name, output_names=output_names, label_names=label_names)
        self.cls = cls
        self.name = name + "(%s)" % cls

    def update(self, labels, preds):
        assert len(preds) == 1
        assert len(labels) == 1

        prob_label = labels[0]
        mask_0 = prob_label == self.cls
        mask_1 = (prob_label == 0) + (prob_label == 1)

        self.sum_metric += mask_0.sum().asnumpy()[0]
        self.num_inst += mask_1.sum().asnumpy()[0]


class MtcnnClsAcc(mx.metric.EvalMetric):
    def __init__(self, cls, name='cls_acc', output_names=('mtcnn_prob',), label_names=('prob_label',)):
        super(MtcnnClsAcc, self).__init__(name, output_names=output_names, label_names=label_names)
        self.cls = cls
        self.name = name + "(%s)" % cls

    def update(self, labels, preds):
        assert len(preds) == 1
        assert len(labels) == 1

        prob = preds[0]
        prob_label = labels[0]

        pred_label = mx.nd.argmax(prob, axis=1).asnumpy().astype('int32')
        label = prob_label.asnumpy().astype('int32')
        mask = prob_label.asnumpy().astype('int32') == self.cls

        self.sum_metric += ((pred_label == label) * mask).sum()
        self.num_inst += mask.sum()


class MtcnnRegrMae(mx.metric.EvalMetric):
    def __init__(self, name='regr_mae', output_names=('mtcnn_regr',), label_names=('prob_label', 'regr_label')):
        super(MtcnnRegrMae, self).__init__(name, output_names=output_names, label_names=label_names)

    def update(self, labels, preds):
        assert len(labels) == 2
        assert len(preds) == 1

        pred = preds[0].asnumpy()
        prob_label = labels[0].asnumpy()
        regr_label = labels[1].asnumpy()
        mask = (prob_label == -1).reshape((-1, 1))

        self.sum_metric += np.abs((regr_label - pred) * mask).sum()
        self.num_inst += mask.sum() * pred.shape[1]


class MtcnnLmksMae(mx.metric.EvalMetric):
    def __init__(self, name='lmks_mae', output_names=('mtcnn_lmks',), label_names=('prob_label', 'lmks_label')):
        super(MtcnnLmksMae, self).__init__(name, output_names=output_names, label_names=label_names)

    def update(self, labels, preds):
        assert len(labels) == 2
        assert len(preds) == 1

        pred = preds[0].asnumpy()
        prob_label = labels[0].asnumpy()
        lmks_label = labels[1].asnumpy()
        mask = (prob_label == -2).reshape((-1, 1))

        self.sum_metric += np.abs((lmks_label - pred) * mask).sum()
        self.num_inst += mask.sum() * pred.shape[1]
