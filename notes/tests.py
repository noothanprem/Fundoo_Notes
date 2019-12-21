import pdb

from django.test import TestCase

# Create your tests here.
import json
#
# import requests
from decouple import config
# from django.test import TestCase
#
# from .models import Label
# with open("test.json") as f:
#     data = json.load(f)
from django.urls import reverse

from .models import Label, Note
from django.contrib.auth.models import User
from django.test import Client
client = Client()

header = {
    'HTTP_AUTHORIZATION': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTc1NjMzMzIyLCJqdGkiOiI2MzE3NTI5Mzk3ZGE0OTMxYjFmYWNlNzRiN2I0YWJmNiIsInVzZXJfaWQiOjN9.g2MxwZtku38dZWL45xWDntim3LQe657U3ABXoXgYzSk'}
# headers = {
#    'Content_Type': "application/json",
#    'Authorization': "TEST_TOKEN"
# }
BASE_URL = config('BASE_URL')


# class TestNote(TestCase):
#     fixtures = ['sahdhd']
#
#     def test_note_post1(self):
#         url = BASE_URL + (data[0]['urls']['createnote'])
#         input = data[0]['notepost1']
#         response = requests.post(url=url, data=input, headers=headers)
#         assert response.status_code == 200
#
#     def test_note_post2(self):
#         url = BASE_URL + (data[0]['urls']['createnote'])
#         input = data[0]['notepost2']
#         response = requests.post(url=url, data=input, headers=headers)
#         assert response.status_code == 200
#
#     def test_note_post3(self):
#         url = BASE_URL + (data[0]['urls']['createnote'])
#         input = data[0]['notepost3']
#         response = requests.post(url=url, data=input, headers=headers)
#         assert response.status_code == 200
#
#     def test_note_post4(self):
#         url = BASE_URL + (data[0]['urls']['createnote'])
#         input = data[0]['notepost4']
#         response = requests.post(url=url, data=input, headers=headers)
#         assert response.status_code == 400
#
#     def test_note_get1(self):
#         url = BASE_URL + (data[0]['urls']['updatenote']) + "/" + (data[0]['noteget1']['note_id'])
#         response = requests.get(url=url, headers=headers)
#         assert response.status_code == 400
#
#     def test_note_get2(self):
#         url = BASE_URL + (data[0]['urls']['updatenote']) + "/" + (data[0]['noteget2']['note_id'])
#         response = requests.get(url=url, headers=headers)
#         assert response.status_code == 404
#
#     def test_note_get3(self):
#         url = BASE_URL + (data[0]['urls']['updatenote']) + "/" + (data[0]['noteget3']['note_id'])
#         response = requests.get(url=url, headers=headers)
#         assert response.status_code == 200
#
#     def test_note_delete1(self):
#         url = BASE_URL + (data[0]['urls']['updatenote']) + "/" + (data[0]['notedelete1']['note_id'])
#         response = requests.delete(url=url, headers=headers)
#         assert response.status_code == 400
#
#     def test_note_delete2(self):
#         url = BASE_URL + (data[0]['urls']['updatenote']) + "/" + (data[0]['notedelete2']['note_id'])
#         response = requests.delete(url=url, headers=headers)
#         assert response.status_code == 404
#
#     def test_note_delete3(self):
#         url = BASE_URL + (data[0]['urls']['updatenote']) + "/" + (data[0]['notedelete3']['note_id'])
#         response = requests.delete(url=url, headers=headers)
#         assert response.status_code == 200
#
#     def test_note_put1(self):
#         url = BASE_URL + (data[0]['urls']['updatenote']) + "/" + (data[0]['noteput1']['note_id'])
#         input = data[0]['noteputdata1']
#         response = requests.put(url=url, data=input, headers=headers)
#         assert response.status_code == 400
#
#     def test_note_put2(self):
#         url = BASE_URL + (data[0]['urls']['updatenote']) + "/" + (data[0]['noteput2']['note_id'])
#         input = data[0]['noteputdata1']
#         response = requests.put(url=url, data=input, headers=headers)
#         assert response.status_code == 404
#
#     def test_note_put3(self):
#         url = BASE_URL + (data[0]['urls']['updatenote']) + "/" + (data[0]['noteput3']['note_id'])
#         input = data[0]['noteputdata1']
#         response = requests.put(url=url, data=input, headers=headers)
#         assert response.status_code == 400
#
#
# class TestLabel:
#
#     def test_label_get1(self):
#         url = BASE_URL + (data[0]['urls']['createlabel'])
#         response = requests.get(url=url, headers=headers)
#         assert response.status_code == 200
#
#     def test_label_get2(self):
#         url = BASE_URL + (data[0]['urls']['createlabel'])
#         input = data[0]['labelget2']['label_id']
#         response = requests.get(url=url, data=input, headers=headers)
#         assert response.status_code == 200
#
#     def test_label_put1(self):
#         url = BASE_URL + (data[0]['urls']['updatelabel']) + "/" + (data[0]['labelget2']['label_id'])
#         input = data[0]['labelput2']
#         response = requests.put(url=url, data=input, headers=headers)
#         assert response.status_code == 200
#
#
# class TestTrash:
#
#     def test_trash_get1(self):
#         url = BASE_URL + (data[0]['urls']['trash'])
#         response = requests.get(url=url, headers=headers)
#         assert response.status_code == 200
#
#     def test_trash_get2(self):
#         url = BASE_URL + (data[0]['urls']['trash1'])
#         response = requests.get(url=url, headers=headers)
#         assert response.status_code == 404
#
#
# class TestArchieve:
#
#     def test_archieve_get1(self):
#         url = BASE_URL + (data[0]['urls']['archieve'])
#         response = requests.get(url=url, headers=headers)
#         assert response.status_code == 200
#
#     def test_archieve_get2(self):
#         url = BASE_URL + (data[0]['urls']['archieve1'])
#         response = requests.get(url=url, headers=headers)
#         assert response.status_code == 404
#
#
# class TestReminder:
#
#     def test_reminder_get1(self):
#         url = BASE_URL + (data[0]['urls']['reminder'])
#         response = requests.get(url=url, headers=headers)
#         assert response.status_code == 200

#     def test_reminder_get2(self):
#         url = BASE_URL + (data[0]['urls']['reminder1'])
#         response = requests.get(url=url, headers=headers)
#         assert response.status_code == 404

# class ModeslTest(TestCase):
#
#     def test_label_string_representation1(self):
#         label = Label(name="My Label1")
#         self.assertEqual(str(label), label.name)
#
#     def test_label_string_representation2(self):
#         label = Label(name="My Label2")
#         self.assertNotEqual(str(label), "")
#
#     def test_label_equal1(self):
#         label1 = Label(name="Mine1")
#         label2 = Label(name="Mine")
#         self.assertFalse(label1 == label2)
#
#     def test_label_equal2(self):
#         label1 = Label(name="My name1")
#         label2 = Label(name="")
#         self.assertFalse(label1 == label2)
#
#     def test_label_isinstance1(self):
#         user1 = User(username="nipun")
#         label1 = Label(name="My new Label1")
#         self.assertFalse(user1 == label1)
#
#     def test_label_isinstance2(self):
#         user1 = User(username="nipun")
#         label1 = Label(name="second label1")
#         self.assertFalse(user1 == label1)
#
#     def test_label_verbose_name_plural1(self):
#         self.assertEqual(str(Label._meta.verbose_name_plural), "labels")
#
#     def test_label_verbose_name_plural2(self):
#         self.assertNotEqual(str(Label._meta.verbose_name_plural), "hello")
#
#     def test_label_verbose_name(self):
#         self.assertEqual(str(Label._meta.verbose_name), "label")
#
#     def test_label_verbose_name(self):
#         self.assertNotEqual(str(Label._meta.verbose_name), "hello")
#
#     def test_note_string_representation1(self):
#         note = Note(title="My title1")
#         self.assertEqual(str(note), note.title)
#
#     def test_note_string_representation2(self):
#         note = Note(title="My note1")
#         self.assertNotEqual(str(note), "")
#
#     def test_note_equal1(self):
#         note1 = Note(title="Mine1")
#         note2 = Note(title="Mine1")
#         self.assertFalse(note1 == note2)
#
#     def test_note_equal2(self):
#         note1 = Note(title="My name1")
#         note2 = Note(title="")
#         self.assertFalse(note1 == note2)
#
#     def test_note_isinstance1(self):
#         user1 = User(username="nipun")
#         note1 = Note(title="My new note1")
#         self.assertFalse(user1 == note1)
#
#     def test_note_isinstance2(self):
#         user1 = User(username="nipun")
#         note1 = Note(title="second note1")
#         self.assertFalse(user1 == note1)
#
#     def test_note_verbose_name_plural1(self):
#         self.assertEqual(str(Note._meta.verbose_name_plural), "notes")
#
#     def test_note_verbose_name_plural2(self):
#         self.assertNotEqual(str(Note._meta.verbose_name_plural), "hello")
#
#     def test_note_verbose_name(self):
#         self.assertEqual(str(Note._meta.verbose_name), "note")
#
#     def test_note_verbose_name(self):
#         self.assertNotEqual(str(Note._meta.verbose_name), "hello")
#
#     def test_reminder_get2(self):
#         url = BASE_URL + "notes_reminder"
#         response = self.client.get(url)
#         print(response.status_code)
#         assert response.status_code == 200


class NoteTest(TestCase):
    fixtures = ['fixtures/db']


    def test_login(self):
        url = "http://127.0.0.1:8000/" + reverse('login_view')
        # print(header)
        response = self.client.post(url, {"username": "admin", "password": "admin"}, content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_label_get1(self):
        url = BASE_URL + reverse('createlabel_view')
        # pdb.set_trace()
        response = self.client.get(url, content_type='application/json', **header)
        # print(response.text)
        self.assertEqual(response.status_code, 200)

    def test_label_post1(self):
        url = BASE_URL + reverse('createlabel_view')
        data = {"name": ""}
        response = self.client.post(url, data, content_type='application/json', **header)
        self.assertEqual(response.status_code, 200)
    def test_label_post2(self):
        url = BASE_URL + reverse('createlabel_view')
        data = {"name": "hello"}
        response = self.client.post(url,data,content_type='application/json',**header)
        self.assertEqual(response.status_code,200)
    def test_label_post3(self):
        url = BASE_URL + reverse('createlabel_view')
        data = {"name" : "hai"}
        response = self.client.post(url,data,content_type='application/json',**header)
        self.assertEqual(response.status_code,200)
    def test_label_put1(self):
        url = BASE_URL + reverse('updatelabel_view',args=[1])
        data = {"name" : "hello"}
        response = self.client.put(url,data,content_type='application/json',**header)
        self.assertEqual(response.status_code,200)
    def test_label_put2(self):
        url = BASE_URL + reverse('updatelabel_view',args=[100])
        data = {"name" : "hello"}
        response = self.client.put(url,data,content_type='application/json',**header)
        self.assertEqual(response.status_code,200)
    def test_label_put3(self):
        url = BASE_URL + reverse('updatelabel_view',args=["sariga"])
        data = {"name" : "hello"}
        response = self.client.put(url,data,content_type='application/json',**header)
        self.assertEqual(response.status_code,200)
    def test_label_delete1(self):
        url = BASE_URL + reverse('updatelabel_view',args=[3])
        response = self.client.delete(url,content_type='application/json',**header)
        self.assertEqual(response.status_code,404)
    def test_label_delete2(self):
        url = BASE_URL + reverse('updatelabel_view',args=["hamweck"])
        response = self.client.delete(url,content_type='application/json',**header)
        self.assertEqual(response.status_code,404)
    def test_label_delete3(self):
        url = BASE_URL + reverse('updatelabel_view',args=["hampadfgn"])
        response = self.client.delete(url,content_type='application/json',**header)
        self.assertEqual(response.status_code,404)

    def test_note_getall(self):
        url = BASE_URL + reverse('createnote_view')
        response = self.client.get(url, content_type='application/json', **header)
        self.assertEqual(response.status_code, 200)
    def test_note_get1(self):
        url = BASE_URL + reverse('updatenote_view',args=[1])
        response = self.client.get(url, content_type='application/json', **header)
        self.assertEqual(response.status_code, 200)
    def test_note_get2(self):
        url = BASE_URL + reverse('updatenote_view',args=["jacks"])
        response = self.client.get(url, content_type='application/json', **header)
        self.assertEqual(response.status_code, 200)
    def test_note_post1(self):
        url = BASE_URL + reverse('createnote_view')
        data = {"title":"test_note2","note":"helloo1","label":["hosur"]}
        response = self.client.post(url, data, content_type='application/json', **header)
        self.assertEqual(response.status_code,400)
    def test_note_post2(self):
         url = BASE_URL + reverse('createnote_view')
         data = {"title":"test_note2","note":"helloo1","label":[123]}
         response = self.client.post(url, data, content_type='application/json', **header)
         self.assertEqual(response.status_code,400)
    def test_note_post3(self):
        url = BASE_URL + reverse('createnote_view')
        data = {"title":"test_note1","note":"helloo1","is_archieve":'true'}
        response = self.client.post(url, data, content_type='application/json', **header)
        self.assertEqual(response.status_code,400)
    def test_note_put1(self):
        url = BASE_URL + reverse('updatenote_view',args=[1])
        data = {"title":"updated_note_1","note":"helloo1", "label":['hosur'],"url":"https://www.facebook.com/"}
        response = self.client.put(url, data, content_type='application/json', **header)
        self.assertEqual(response.status_code, 400)
    def test_note_put2(self):
        url = BASE_URL + reverse('updatenote_view',args=[1])
        data = {"title":"updated_note_2","note":"helloo1", "label":['hosur'],"is_archieve":"false"}
        response = self.client.put(url, data, content_type='application/json', **header)
        self.assertEqual(response.status_code, 400)

    def test_note_delete1(self):
        url = BASE_URL + reverse('updatenote_view',args=[3])
        response = self.client.delete(url, content_type='application/json', **header)
        self.assertEqual(response.status_code, 400)
    def test_note_delete2(self):
        url = BASE_URL + reverse('updatenote_view',args=["hellooo"])
        response = self.client.delete(url, content_type='application/json', **header)
        self.assertEqual(response.status_code, 400)

    def test_note_share1(self):
        url = BASE_URL + reverse('noteshare_view')
        data = {"title":"sharing_note1","note":"note1"}
        response = self.client.post(url,data,content_type='application/json', **header)
        self.assertEqual(response.status_code,200)
    def test_note_share2(self):
        url = BASE_URL + reverse('noteshare_view')
        data = {"title":"sharing_note2"}
        response = self.client.post(url,data,content_type='application/json', **header)
        self.assertEqual(response.status_code,404)



    def test_reminder(self):
        url = BASE_URL + reverse('reminderview')
        response = self.client.get(url,content_type='application/json',**header)
        self.assertEqual(response.status_code,200)
    def test_trash(self):
        url = BASE_URL + reverse('trashview')
        response = self.client.get(url, content_type='application/json', **header)
        self.assertEqual(response.status_code,200)
    def test_archieve(self):
        url = BASE_URL + reverse('archieveview')
        response = self.client.get(url, content_type='application/json', **header)
        self.assertEqual(response.status_code,200)

