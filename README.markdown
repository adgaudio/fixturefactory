
Child classes must inherit from BaseFactory, must have a getparams method and must define a model variable.  
It's helpful to adhere to the following template:

    *model is the class we are mass instantiating
    *getparams: see FactoryMixin.getparams.__doc__

    *if you want by default to not save to db, override init
     with following: super(...).__init__(save_to_db=False)
    *if you override __init__,
        you need to call super(...).__init__ in the last line


Use Cases:

# creating objects
>>> ChildFactory()
>>> ChildFactory(save_to_db=False)

>>> child2 = ChildFactory().last_obj_created
>>> child3 = ChildFactory().last_obj_created

# dynamically passing params to create certain kinds of connections
>>> BrotherFactory(child2.pk, child3.pk)


Defining your Factories: All factories you create need to have these basic characteristics:
===

* Must inherit from BaseFactory (should also inherit from FactoryMixin to simplify working with Django)
* Must have a class variable, model, which returns the class object we want to mass instantiate
* Must have a method, getparams, which returns a dict containing the params necessary to instantiate the model.

The basic template looks like this:

    class ChildFactory(BaseFactory, FactoryMixin):
        model = myapp.models.SomeModel

        def getparams(self): return {}


Example Implementations:

The following factory generates generic Django users.  A more advanced implementation may make use of randomly generated text, etc.  Note that getparams returned locals(), which is a dict of the local environment.  If you have temporary variables, this approach can cause django to raise an exception, but it also brings up the point that getparams() probably should be doing anything complicated.

    class UserFactory(BaseFactory, FactoryMixin):
        model = django.contrib.auth.models.User

        def getparams(self):
            pk = self.getUnusedPk() # Utilize the methods in FactoryMixin
            username = 'markov_%s' % pk
            password = username
            return locals()

This next example shows how to implement Foreign Keys, where the UserProfile has a Foreign Key on the above User model.  Note that the 'user' variable in getparams() is an instance of the UserFactory's own class variable, model 

    class UserProfileFactory(BaseFactory, FactoryMixin):
        model = myapp.models.UserProfile

        def getparams(self):
            """An example of a foreign key"""
            user = UserFactory().last_obj_created
            pk = user.pk #this User and UserProfile share the same primary key


There are a couple options for Many to Many Relationships.  In the simplest form, they can follow the same form as above if you don't care about which 2 UserProfiles the relationships are between.  

    class RelatedUserFactory(BaseFactory, FactoryMixin):
        model = myapp.models.RelatedUser
        def getparams(self):
            user1 = self.getRandInst(myapp.models.UserProfile).pk
            user2 = self.getRandInst(myapp.models.UserProfile).pk
            return locals()

A second, more complex option (helpful for m2m relationships): Dynamically passing in parameters to your factory class at time of execution.  Note that in this example, we call the BaseFactory __init__ method AFTER defining self.pk1 and self.pk2.  This is an important gotcha and exists because the BaseFactory's __init__ method currently calls child factory's getparams() method.

    class RelatedUserFactory(BaseFactory, FactoryMixin):
        model = myapp.models.RelatedUser

        def __init__(pk1, pk2, *args, **kwargs):
            self.pk1 = pk1
            self.pk2 = pk2
            super(RelatedUserFactory, self).__init__(*args, **kwargs)

        def getparams(self):
            user1 = self.pk1
            user2 = self.pk2
            return locals()

