from django.contrib.auth.models import Group,User
from models import Category, Team, Project, Category_value, Query, Query_properties


def initialize():
    if Category.objects.all():
        print ("The database is already initialized")
    else:
        print ("The database is empty")
        #These properties are the default categories a user is called to use (obligatory)
        categoryK = Category.objects.create(name="Keywords")
        categoryK.save()
        categoryT = Category.objects.create(name="Twitter")
        categoryT.save()
        categoryF = Category.objects.create(name="Facebook")
        categoryF.save()
        #TODO remove categoryR completely
        categoryR = Category.objects.create(name="RSS")
        categoryR.save()

        ## Data below are only for development purposes!!

        # user = User.objects.create(username="test1",password="foo")
        # user.save()
        # team = Team.objects.create(name="AIDIMA-team", created_by=user)
        # team.save()
        # project = Project.objects.create(name="Social Enabler", created_by=user, owned_by=team)
        # project.save()
        # value1 = Category_value.objects.create(value="coolfurniture, cool furniture, sofa, bed, living room, leather", category=categoryK, owned_by=project)
        # value1.save()
        # value2 = Category_value.objects.create(value="aidima, IKEA, neoset", category=categoryT, owned_by=project)
        # value2.save()
        # value3 = Category_value.objects.create(value="http://www.facebook.com/aidima", category=categoryF, owned_by=project)
        # value3.save()
        # value4 = Category_value.objects.create(value=" ", category=categoryR, owned_by=project)
        # value4.save()

        # #extend for queries
        # categoryM = Category.objects.create(name="materials")
        # categoryM.save()
        # value5 = Category_value.objects.create(value="leather, cotton", category=categoryM, owned_by=project)
        # value5.save()
        # #query
        # query1 = Query.objects.create(name="italian sofas",venn="or", from_date="2013-10-01T09:00:00+03:00",to_date="2013-10-20T09:00:00+03:00", created_by=user, owned_by=project )
        # query1.save()
        # queryprop11=Query_properties.objects.create(query=query1,category=categoryT, properties="aidima")
        # queryprop11.save()
        # queryprop12=Query_properties.objects.create(query=query1,category=categoryK, properties="sofa, bed, italian")
        # queryprop12.save()
        # #query
        # query2 = Query.objects.create(name="living room",venn="or", from_date="2013-09-01T09:00:00+03:00",to_date="2013-10-24T09:00:00+03:00", created_by=user, owned_by=project )
        # query2.save()
        # queryprop21=Query_properties.objects.create(query=query2,category=categoryT, properties="aidima, IKEA")
        # queryprop21.save()
        # queryprop22=Query_properties.objects.create(query=query2,category=categoryK, properties="living room, italian")
        # queryprop22.save()

        print ("The database has been initialized")
