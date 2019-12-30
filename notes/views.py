from __future__ import unicode_literals

import json
import logging
import os
import pdb

from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.decorators import method_decorator
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q
from rest_framework.generics import GenericAPIView
from django.utils import timezone
from fundoo.settings import file_handler
from .decorators import login_decorator
# from django.utils import timezone
# from notes.tasks import send_feedback_email_task
from .documents import NotesDocument
from .lib.amazon_s3_file import UploadImage
from .lib.redis_function import RedisOperation
from .models import Note
from .serializers import UploadImageSerializer, NoteShareSerializer, NoteSerializer, LabelSerializer, \
    NotesSearchSerializer
from .service.label import LabelOperations
from .service.note import NoteOperations
from utility import Response
# from .background_tasks import hello

redisobject = RedisOperation()

response_class_object = Response()
uploadclassobject = UploadImage()
labelobject = LabelOperations()
noteobject = NoteOperations()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
from .background_tasks import hello
class UploadImage(GenericAPIView):
    serializer_class = UploadImageSerializer


    def post(self, request):

        """
        :param request: gives the image for upload
        :return: uplads the images into s3 bucket
        """
        try:
            image = request.FILES.get('imgs')
            response = uploadclassobject.upload_file(image)
            final_response = response_class_object.json_response(response)
            return HttpResponse(final_response)
        except Exception:
            response = response_class_object.smd_response(False, 'Upload unsuccessful', '')
            final_response = response_class_object.json_response(response)
            return HttpResponse(final_response)


# API for sharing of notes
@method_decorator(login_decorator, name='dispatch')
class NoteShare(GenericAPIView):
    serializer_class = NoteShareSerializer


    def post(self, request):
        """
        :param request: to share the note to social media
        :return: shares to social media
        """
        try:
            title = request.data['title']
            note = request.data['note']
        except Exception:
            logger.error("Exception occured")
            response = response_class_object.smd_response(False,"Exception occured",'')
            final_response = response_class_object.json_response(response)
            return HttpResponse(final_response,status=404)
        if title == "" or note == "":
            response = response_class_object.smd_response(False, 'Please fill the fields', '')
            final_response = response_class_object.json_response(response)
            return HttpResponse(final_response)
        return render(request, 'notes_upload.html', {'title': title, 'note': note})


@method_decorator(login_decorator, name='dispatch')
class Trash(GenericAPIView):
    serializer_class = NoteSerializer
    def get(self, request):
        """
        :param request: requests for the notes in the trash
        :return: returns the notes in the trash
        """

        user = request.user
        user_id = user.id
        response = noteobject.get_trash(user)


        final_response = response_class_object.json_response(response)
        if response['success'] == True:
            return HttpResponse(final_response)
        else:
            return HttpResponse(final_response,status = 400)


@method_decorator(login_decorator, name='dispatch')
class Archieve(GenericAPIView):
    serializer_class = NoteSerializer
    def get(self, request):
        """
        :param request: requests for the archieved note
        :return: returns the archieved notes
        """
        user = request.user
        response = noteobject.get_archieved_notes(user)
        final_response = response_class_object.json_response(response)
        if response['success'] == True:
            return HttpResponse(final_response)
        else:
            return HttpResponse(final_response,status = 400)


@method_decorator(login_decorator, name='dispatch')
class Reminder(GenericAPIView):


    def get(self, request):
        """
        :param request: to get the reminders
        :return: returns the reminders lists
        """

        user = request.user
        response = noteobject.get_reminders(user)
        final_response = response_class_object.json_response(response)
        if response['success'] == True:
            return HttpResponse(final_response)
        else:
            return HttpResponse(final_response,status=400)


@method_decorator(login_decorator, name='dispatch')
class CreateLabel(GenericAPIView):
    serializer_class = LabelSerializer


    def get(self, request):
        """
        :param request: requests for label
        :return: returns the label data
        """
        user = request.user
        response_from_get_label = labelobject.get_label(user)
        final_response = response_class_object.json_response(response_from_get_label)
        if response_from_get_label['success'] == False:
            return HttpResponse(final_response,status = 404)
        else:
            return HttpResponse(final_response,status = 200)

    def post(self, request):
        """
        :param request: requests to create a label
        :return: creates a label and returns the new label data
        """
        user = request.user
        data = request.data
        response_from_create_label = labelobject.create_label(user,data)
        final_response = response_class_object.json_response(response_from_create_label)
        if not response_from_create_label['success']:
            return HttpResponse(final_response,status = 404)
        else:
            return HttpResponse(final_response,status = 200)



@method_decorator(login_decorator, name='dispatch')
class UpdateLabel(GenericAPIView):
    serializer_class = LabelSerializer


    def put(self, request, label_id):
        """
        :param request: requests to update a particular label
        :param label_id: id of the label to update
        :return: updates the label and returns the new label data
        """
        user = request.user
        request_body = request.body
        response = labelobject.update_label(user,request_body,label_id)
        final_response = response_class_object.json_response(response)
        if response['success'] == False:
            return HttpResponse(final_response, status=400)
        else:
            return HttpResponse(final_response, status=200)

    def delete(self, request, label_id):

        """
        :param request: requests to delete a particular label
        :param label_id: id of the label to delete
        :return: deletes the label
        """
        user = request.user
        response = labelobject.delete_label(user, label_id)
        final_response = response_class_object.json_response(response)
        if response['success'] == False:
            return HttpResponse(final_response,status=404)
        else:
            return HttpResponse(final_response,status=200)

@method_decorator(login_decorator, name='dispatch')
class CreateNote(GenericAPIView):
    serializer_class = NoteSerializer


    def get(self, request):
        """
        :param request: requests to get a note
        :return: returns the new note data
        """

        all_notes = Note.objects.all()
        page = request.GET.get('page')
        paginator = Paginator(all_notes, 2)

        try:
            notes = paginator.page(page)
        except PageNotAnInteger:
            logger.warning("got error for getting note for user %s", str(PageNotAnInteger))
            notes = paginator.page(1)
        except EmptyPage:
            logger.warning("got error for getting note", EmptyPage)
            notes = paginator.page(paginator.num_pages)
        logger.info("all the notes are rendered to html page")

        return render(request, 'note_list.html', {'notes': notes})

    def post(self, request):
        """
        :param request: requests to create a note with the given data
        :return: returns the new note data
        """
        response = noteobject.create_note(request)
        final_response = response_class_object.json_response(response)
        if response['success'] == False:

            return HttpResponse(final_response, status=400)
        else:
            return HttpResponse(final_response, status=200)

@method_decorator(login_decorator, name='dispatch')
class UpdateNote(GenericAPIView):
    serializer_class = NoteSerializer


    def get(self, request, note_id):

        """
        :param request: requests for a particular note data
        :param note_id: id of the note
        :return: returns the requested note datas
        """
        user = request.user
        response = noteobject.get_note(user, note_id)
        final_response = response_class_object.json_response(response)
        if (response['success'] == False):
            return HttpResponse(final_response, status=400)
        else:
            return HttpResponse(final_response, status=200)

    def put(self, request, note_id):

        """
        :param request: requests to update a particular note
        :param note_id: id of the note to update
        :return: updates the note and returns the updated data
        """
        user =  request.user
        request_data = request.data
        response = noteobject.update_note(user,request_data, note_id)
        final_response = response_class_object.json_response(response)
        if (response['success'] == False):
            return HttpResponse(final_response, status=400)
        else:
            return HttpResponse(final_response)

    def delete(self, request, note_id):

        """
        :param request: requests to delete a particular note
        :param note_id: id of the note to delete
        :return: deletes the note
        """
        user = request.user
        response = noteobject.delete_note(user, note_id)
        final_response = response_class_object.json_response(response)
        if (response['success'] == False):

            return HttpResponse(final_response, status=400)
        else:

            return HttpResponse(final_response)


class ImageLoading(GenericAPIView):
    def get(self, request):
        return render(request, 'lazy_loading.html')




class ReminderNotification(GenericAPIView):
    serializer_class = NoteSerializer

    def get(self,request):

        response = noteobject.reminder_notification()
        final_response = response_class_object.json_response(response)
        return HttpResponse(final_response)

class NewNotification(GenericAPIView):
    serializer_class = NoteSerializer

    def get(self,request):
        subject = "Note Reminder"
        message = render_to_string('note_reminder_email.html')
        sender = os.getenv('EMAIL_HOST_USER')
        reciever = os.getenv('EMAILID')

        send_mail(subject, message, sender, [reciever])
        print("mail send")
        response={'success':True,'message':"notification",'data':''}
        return HttpResponse(json.dumps(response))

@method_decorator(login_decorator, name='dispatch')
class NotesSearch(GenericAPIView):

    serializer_class = NotesSearchSerializer

    def get(self,request,query_data):

        client = Elasticsearch()
        search = NotesDocument.search()

        #note_data=search.filter('multi_match', note = note)
        #note_data=MultiMatch(query=note, fields=['title', 'note','label'])
        #note_data = Q("multi_match", query=note, fields=['title', 'note'])
        # note_data = search.query(
        #     {
        #                 "bool": {
        #                     "must": [
        #                         {"multi_match": {
        #                             "query": title,
        #                             "fields": ["label.name", 'title', 'note', 'reminder', 'color']
        #                         }},
        #                     ],
        #                     "filter": [
        #                         {"term": {"user.username": str(request.user)}}
        #                     ]
        #                 }
        #             }
        # )


        query_result = Q("multi_match", query=query_data, fields=['title', 'note','label.name','reminder','color'])
        note_data = search.query(query_result)
        #pdb.set_trace()
        new_note_data = NotesSearchSerializer(note_data.to_queryset(), many=True)
        print("note data : ",new_note_data)
        response = response_class_object.smd_response(True,"Successfully fetched notes",new_note_data.data)
        final_response = response_class_object.json_response(response)
        return HttpResponse(final_response)

class BackgroundTasks(GenericAPIView):
    serializer_class = NoteSerializer


    def get(self,request):
        hello()
        response = response_class_object.smd_response(True, "Successfully fetched notes", '')
        final_response = response_class_object.json_response(response)
        return HttpResponse(final_response)



