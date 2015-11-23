from django.db import models
from django.contrib.auth.models import User

#Every user has a team
class Team(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)
    created_by = models.ForeignKey(User, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    class Admin:
        pass

    def __unicode__(self):
        return "%s" % self.name


class Project(models.Model):
    name = models.CharField(max_length=255, blank=False)
    created_by = models.ForeignKey(User, blank=False)
    owned_by = models.ForeignKey(Team, null=True, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    class Admin:
        pass

    def __unicode__(self):
        return "%s" % self.name


# Accounts, Keywords, Materials, Companies
class Category(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)

    class Admin:
        pass

    def __unicode__(self):
        return "%s" % self.name

# Every Group may create a series of values for the categories
class Category_value(models.Model):
    value = models.TextField(max_length=255, blank=True)
    category = models.ForeignKey(Category, blank=False)
    owned_by = models.ForeignKey(Project, blank=False)

    class Admin:
        pass

    def __unicode__(self):
        return "%s : %s : %s" % (self.category.name, self.owned_by.name,self.value)


class Query(models.Model):
    name = models.TextField(max_length=255, null=True, blank=True)
    venn = models.CharField(max_length=5, default="OR", blank=False, )
    #query = models.TextField(null=True, blank=True)  # JSON query
    from_date = models.DateTimeField(null=True, blank=True)
    to_date = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, blank=False)
    owned_by= models.ForeignKey(Project, blank=False)

    class Admin:
        pass

    def __unicode__(self):
        return "%s" % self.name


class Query_properties(models.Model):
    query = models.ForeignKey(Query, blank=False)
    category = models.ForeignKey(Category, blank=False) #name of category
    properties = models.TextField(max_length=400, null=False, blank=False) #properties of category

    def __unicode__(self):
        return "%s : %s" % (self.query, self.category)

class Query_languages(models.Model):
    query = models.ForeignKey(Query, blank=False)
    language = models.TextField(max_length=10, null=False, blank=False)
    def __unicode__(self):
        return "%s : %s" % (self.query, self.language)

# cache results to improve system performance and require refresh for update
class Results(models.Model):
    query = models.ForeignKey(Query, blank=False)
    results = models.TextField(null=True, blank=True)  # JSON result
    updated = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s" % self.query



