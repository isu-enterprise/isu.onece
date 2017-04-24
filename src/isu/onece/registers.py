from .interfaces import IDocument, IAccumulatorRegister


class AccumulatorRegister(object):
    """Accumulates amounts by means of
    accumulating document'S data.
    """

    def __init__(self):
        super(AccumulatorRegister, self).__init__()
