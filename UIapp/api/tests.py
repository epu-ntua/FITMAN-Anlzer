from django.test import TestCase
from django.contrib.auth.models import User, Group
from selenium import webdriver

from UIapp.models import Project, Query


class APITestCase(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="sample group")
        self.user = User.objects.create(username="koukli", email="mpetyx2@gmail.com")
        self.browser = webdriver.Firefox()
        self.project = Project.objects.create(name="sample group", created_by=self.user)
        self.report = Query.objects.create(name="sample report", created_by=self.user, owned_by=self.project)
        self.user.groups.add(self.group)

    def test_group_user(self):
        response = self.client.get('/api/group/%d/user/%d' % (self.group.id, self.user.id))
        # print(response)
        # pprint(response.__dict__)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response._container), 1)

    def test_group_user_handle(self):
        response = self.client.get('/api/group/%d/user' % self.group.id)
        # print(response)
        # pprint(response.__dict__)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response._container), 1)

    def test_group_user_handle_privileges(self):
        response = self.client.get('/api/group/%d/user/%d/privileges' % (self.group.id, self.user.id))
        # print(response)
        # pprint(response.__dict__)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response._container), 1)

    def test_project_train(self):
        response = self.client.get('/api/project/%d/train$'%self.project.id)
        # print(response)
        # pprint(response.__dict__)
        self.assertEqual(response.status_code,200)
        # self.assertEqual(len(response._container),1)
        # pass

    def test_project_status(self):
        response = self.client.get('/api/project/%d/status' % self.project.id)
        # print(response)
        # pprint(response.__dict__)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(response._container),1)

    def test_project_group(self):
        response = self.client.get('/api/project/%d/group' % self.project.id)
        # print(response)
        # pprint(response.__dict__)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(response._container),1)

    def test_project_stream(self):
        response = self.client.get('/api/project/%d/stream' % self.project.id)
        # print(response)
        # pprint(response.__dict__)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(response._container),1)

    def test_project_reports(self):
        response = self.client.get('/api/project/%d/report' % self.project.id)
        # print(response)
        # pprint(response.__dict__)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(response._container),1)

    def test_project_report(self):
        response = self.client.get('/api/project/%d/report/%d' % (self.project.id, self.report.id))
        # print(response)
        # pprint(response.__dict__)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(response._container),1)

    def test_project_report_results(self):
        response = self.client.get('/api/project/%d/report/%d/results' % (self.project.id, self.report.id))
        # print(response)
        # pprint(response.__dict__)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(response._container),1)

    def tearDown(self):
        self.user.delete()
        self.group.delete()
        self.browser.quit()
