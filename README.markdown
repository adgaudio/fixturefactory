About:
===

fixturefactory is a super simple, easy to use and customizable library for creating Django fixtures.  

Within fixturefactory.py, you will find a BaseFactory and DjangoMixin.

* The BaseFactory class was written to make developing with factories for other purposes or frameworks very simple.
* The DjangoMixin class provides some methods to make fixture creation easy.

Please fork, give feedback, or add an issue to the tracker!

Use Cases:
===

Creating instances of a model

    >>> ChildFactory()
    >>> ChildFactory(save_to_db=False)

Dynamically passing params to your factories

    >>> child1 = ChildFactory().last_obj_created
    
    >>> BrotherFactory(pk1=child1.pk, pk2=1) # These pks are usable as class vars by BrotherFactory.getparams()


Defining your Factories: All factories you create need to have these basic characteristics:
===

* Must inherit from BaseFactory (should also inherit from DjangoMixin to simplify working with Django)
* Must have a class variable, 'model', which works like this: inst = model(some='keyword args') ; inst.save() # to db
* Must have a method, 'getparams', which returns a dict containing the params necessary to instantiate the model.

The basic template looks like this:

    class ChildFactory(BaseFactory, DjangoMixin):
        model = myapp.models.SomeModel

        def getparams(self): return {}


Example Implementations:

The following factory generates generic Django users.  A more advanced implementation may make use of randomly generated text, etc.  Note that getparams returns locals(), which is a dict of the local environment.  If you have defined temporary variables in the getparams() method, this approach can cause django to raise an exception, but it also brings up the point that getparams() should not do anything complicated.  The purpose of getparams() is to define parameters that will eventually get sent as a call to your factory's model

    class UserFactory(BaseFactory, DjangoMixin):
        model = django.contrib.auth.models.User

        def getparams(self):
            pk = self.getUnusedPk() # Utilize the methods in DjangoMixin
            username = 'markov_%s' % pk
            password = username
            return locals()

This next example shows how to implement Foreign Keys, where the UserProfile has a Foreign Key on the above example's User model.  Note that the 'user' variable in getparams() is an instance of the UserFactory's model 

    class UserProfileFactory(BaseFactory, DjangoMixin):
        model = myapp.models.UserProfile

        def getparams(self):
            """An example of a foreign key"""
            user = UserFactory().last_obj_created
            pk = user.pk #this User and UserProfile share the same primary key
            return locals()

Implementing Many to Many Relationships are also very easy. In this example, lets assume that RelatedUser is a many to many table linking Users to each other.  Use this simple form if you don't care about which 2 UserProfiles the relationships are between:

    class RelatedUserFactory(BaseFactory, DjangoMixin):
        model = myapp.models.RelatedUser
        def getparams(self):
            user1_id = self.getRandInst(myapp.models.UserProfile).pk
            user2_id = self.getRandInst(myapp.models.UserProfile).pk
            return locals()

If you wanted to link 2 user profiles dynamically at runtime, your factory might look a little different.  Note that this design gives you enormous potential to easily customize how you create objects:

    class RelatedUserFactory(BaseFactory, DjangoMixin):
        model = myapp.models.RelatedUser

        def getparams(self):
            user1 = self.pk1 #NOTE the use of self.pk1 and self.pk2
            user2 = self.pk2
            return locals()

    >>> RelatedUserFactory(pk1=3, pk2=5) #keyword param required in this case.

You can avoid typing in keyword arguments if you really want to by overriding the init method.  If you do this, which probably means you're overthinking things a bit, make sure you call super() **at the end** of your init method like so:

        def __init__(self, pk1, pk2):
            self.pk1 = pk1
            self.pk2 = pk2
            super(self.__class__, self).__init__()

Also, you can have your factory fall back to randomly choosing values if no keyword argument is supplied by setting class variables to None before __init__ gets called.

    class RelatedUserFactory(BaseFactory, DjangoMixin):
        model = mysapp.models.RelatedUser

        pk1 = None # sets default value
        pk2 = None

        def getparams(self):
            user1 = self.pk1 or self.getRandInst().pk # if no pk1 is passed in at time of instantiation, get a random pk
            user2 = self.pk2 or self.getRandInst().pk

Development:
===

To use BaseFactory for a purpose other than Django fixtures, you'd have to (probably) override the BaseFactory.create() method.  You will also probably want to create a mixin to make your factories very simple (see DjangoMixin for an example).

I hope all this encourages you to use fixturefactory!
