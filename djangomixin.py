import random

class DjangoMixin(object):
    """Useful/Necessary methods for Fixture Factories"""

    def _getmodel(self, model=None):
        if model == None:
            return self.model
        return model

    def getSome(self, percent, model=None):
        """Return list of model objects with len equal to
        some percent the len of self.model.objects.all()"""
        model = self._getmodel(model)
        if isinstance(percent, int):
            percent = percent * .1
        percent = 1 - percent
        rv = [x for x in self.model.objects.all() if random.random() > percent]
        return rv

    def getPks(self, model=None):
        """Get flattened list of primary keys"""
        model = self._getmodel(model)
        pks = model.objects.values_list('pk', flat=True)
        return pks

    def getUnusedPk(self, model=None):
        """Get minimum possible unused primary key. HOWEVER,
        Try to return self.pk if _getmodel(model) returns self.model"""
        if self._getmodel(model) == self.model:
            try: return self.pk
            except: pass
        a = set(self.getPks(model)) or [1]
        b = set(range(min(a), max(a)+2))
        return min(b.difference(a))

    def getRandInst(self, model=None):
        """Return randomly selected instance of possible models.  HOWEVER,
        Try to return class var with same name as model, if possible"""
        model = self._getmodel(model)

        # Check if model's name is a class var with first letter lower case
        name = model.__name__[0].lower() + model.__name__[1:]
        if hasattr(self, name):
            return getattr(self, name)

        pks = self.getPks(model)
        if not pks:
            raise IndexError('No primary keys for model: %s' % model)
        pk = random.choice(pks)
        return model.objects.get(pk=pk)

    #def newInstance(self, model=None):
        #""""return self.model.objects.get(pk=sorted(pks)[-1])

