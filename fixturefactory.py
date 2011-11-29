import random

class BaseFactory(object):
    """Base Class for creating django objects """

    last_obj_created = 'None'
    call_lastly = True # call lastly() by default

    def getparams(cls):
        """Template method: must be overridden by child class.
        Return dict of params that get sent to self.create()

        Example logic:

        pk = self.getUnusedPk() # optional
        username = 'markov_%s' % pk
        password = username

        return locals()
        """
        raise NotImplementedError(
                'You cannot directly instantiate BaseFactory '
                'or call this method directly')

    def lastly(cls):
        """ Optional Template method: If used, must be overridden
        by child class.  Contains code to execute after instantiating
        a model object

        Example logic: If my model instance has a many to many field,
        I can add many to many relationships to the instance

        inst = self.last_obj_created
        for x in range(15):
            inst.m2mForSomeModel.add(self.getRandInst( SomeModel ))

        """

    def __init__(self, *args, **kwargs):
        """Create new instance of a model by calling getparams in child class.
        Don't call directly.  Don't instantiate BaseFactory directly.

        Accepts these kwargs (which don't get passed to django model):
            lastly - bool that determines whether or not to call cls.lastly()

        Any other given params get passed to
        ChildCls.getparams(*args, **kwargs)"""

        try:
            call_lastly = kwargs['lastly']
            del kwargs['lastly']
        except: call_lastly = self.call_lastly

        # turn kwargs into class vars so getparams()
        # NOTE: kwargs override getparams(), so this is only useful
        # for things like DjangoMixin methods which need to know
        # which params you will be using
        self.__dict__.update(kwargs)

        # Make dict of params necessary to create object
        dict_ = self.getDefaults() # DEFAULT values

        # Override defaults with getparams()
        tmp = self.getparams()
        dict_.update(tmp)
        self.__dict__.update(tmp)

        #override getparams args with those supplied at runtime
        dict_.update(**kwargs)
        self.__dict__.update(**kwargs)

        try: del dict_['self'] # we don't want to pass this around
        except: pass

        # Create model object
        self.last_obj_created = self.create(**dict_)

        # Execute lastly() unless otherwise specified
        if call_lastly:
            self.lastly()

    def __call__(self):
        """Return last_obj_created when a child class INSTANCE is called"""
        return self.last_obj_created

    def __repr__(self):
        return "%s: last_obj_created <%s>" % (
                self.__class__.__name__, str(self.last_obj_created))

    def create(self, save_to_db=True, **kwargs):
        """A wrapper that uses self.model to create an instance of
        self.model.  Assumes this works: inst=model(**kwargs) and inst.save()

        In Django, this would wrap Django's
        model.objects.create(**kwargs) method."""

        inst = self.model(**kwargs)
        if save_to_db:
            inst.save()
        return inst

    def getDefaults(self):
        """Return dict of default values with which to call self.create().
        These values may be overridden by
            getparams()
            a child class
            runtime parameters
        """
        return dict(save_to_db=True, )

