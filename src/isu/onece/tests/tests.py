from zope.interface import implementer
from isu.onece.interfaces import IVocabularyItem


class TestReferenceBook:

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_minimal(self):
        @implementer(IVocabularyItem)
        class RefBook(object):

            def __init__():
                pass
