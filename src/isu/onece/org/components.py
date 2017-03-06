from isu.onece.interfaces import IVocabulary, IVocabularyItem
from zope.interface import implementer
from zope.component.factory import Factory
from zope.component import getGlobalSiteManager
from zope.component.interfaces import IFactory

@implementer(IVocabularyItem)
class Commonditiy(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

@implementer(IVocabulary)
class Commondities(object):
    def __init__(self, terms=None, factory_name=None):
        if factory_name is None:
            raise ValueError("no factory name supplied")

        if terms is None:
            terms = []

        self.terms = []
        self.factory_name = factory_name

    def append(self, com):
        if IVocabularyItem.providedBy(com):
            self.terms.append(com)
        else:
            raise ValueError("wrong object type")

    def remove(self, com=None, id=None):
        if com in self.terms:
            self.terms.remove(com)
            return com
        if id is not None:
            com = [c for c in self.terms if c.id == id][0]
            self.terms.remove(com)
            return com

commondity_factory=Factory(Commonditiy, 'Commoditiy')

GSM = getGlobalSiteManager()
GSM.registerUtility(commondity_factory, IFactory, 'commondity')

