from zope.interface import implementer
from isu.onece.interfaces import IReferenceBook


class TestReferenceBook:

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_minimal(self):
        @implementer(IReferenceBook)
        class RefBook(object):

            def __init__():
                pass
