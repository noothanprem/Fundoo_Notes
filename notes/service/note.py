import os
import pdb

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import HttpResponse
from notes.models import Note, Label
from notes.lib.redis_function import RedisOperation
from notes.serializers import NoteSerializer, CollaboratorSearializer
from fundoo.settings import file_handler
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
import json
import logging
from django.db.models import Count

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

redisobject = RedisOperation()
redisobject.__connect__()


class NoteOperations:
    response = {"success": False,
                "message": "",
                "data": []}

    def smd_response(self, success, message, data):
        self.response['success'] = success
        self.response['message'] = message
        self.response['data'].append(data)
        return self.response

    """
    Function for creating note
    """

    def create_note(self, request):
        """
        :param request: passes the note datas
        :return: creates note
        """

        try:
            # getting the data from request
            # spdb.set_trace()
            data = request.data  # getting the user
            user = request.user
            user_id = user.id
            # creating the lists for collaborators and labels
            collab_list = []
            label_list = []
            labels = data['label']  # iterates through all the labels in the list
            for label in labels:  # getting each label and adding the label_id to the list
                labelobject = Label.objects.filter(user_id=user_id, name=label)
                if not labelobject:
                    raise Label.DoesNotExist
                label_id = labelobject.values()[0]['id']
                label_list.append(label_id)
                print("label list  : ", label_list)
            # replaces the 'label' in data with the new label_list
            data['label'] = label_list
        except Label.DoesNotExist:
            logger.error("Exception occured while accessing label")
            response = self.smd_response(False, "Exception occured while accessing label", [])
            return response
        except Exception:
            logger.error("Exception occured")
            response = self.smd_response(False, "Exception occured", [])
            return self.response

        try:
            collaborators = data['collaborator']
            # getting the collaborators with the given email
            collaborator_object = User.objects.filter(email__in=collaborators)

            if not collaborator_object:
                raise User.DoesNotExist
            # getting the id of the collaborator
            collaborator_id_list = []
            for collab in collaborator_object:
                collaborator_id_list.append(collab.id)
                print("collaborator id list : ", collaborator_id_list)
            # adding all the ids to the list
            for collaborator_id in collaborator_id_list:
                collab_list.append(collaborator_id)
                print("collaborator list : ", collab_list)

            # replaces in the data with the new list
            data['collaborator'] = collab_list
            print("data : ", data)

        except User.DoesNotExist:

            response = self.smd_response(False, "Exception occured while accessing the user", [])
            return response

        except Exception:
            logger.error("Exception occured")
            response = self.smd_response(False, "Exception occured", [])
            return response

        serializer = NoteSerializer(data=data, partial=True)
        if serializer.is_valid():
            print("Serializer valid ")
            create_note = serializer.save(user=user)

            string_user_id = str(user.id)
            redisobject.hmset(string_user_id + "note", {create_note.id: str(json.dumps(serializer.data))})

            logger.info("note created successfully")
            self.response['success'] = True
            self.response['message'] = "note created successfully"
            self.response['data'].append(data)
            return self.response
        logger.error("note creation failed")

        response = self.smd_response(False, "Note creation failed", [])
        return response

    def get_note(self, user, note_id):
        """
        :param request: to get the note
        :param note_id: id of the note
        :return: returns the note
        """

        try:

            string_user_id = str(user.id)
            redis_data = redisobject.hvals(string_user_id + "note")
            str_note_data = str(redis_data)

            if redis_data is None:
                note = Note.objects.filter(id=note_id)
                note_contents = note.values()

                str_note_data = note_contents[0]
                logger.info("Data accessed from database")

        except Note.DoesNotExist:
            logger.error("Exception occured while accessing Note")

            self.response['message'] = "Exception occured while accessing Note"
            return self.response
        except KeyError:
            logger.error("Key error occured")

            self.response['message'] = "Key error occured"
            return self.response
        except Exception as e:
            logger.error(str(e))
            self.response['message'] = str(e)
            return self.response

        logger.info("Data accessed from redis")
        self.response['success'] = True
        self.response['message'] = "Read Operation Successful"
        self.response['data'].append(str_note_data)
        return self.response

    def update_note(self, user, request_data, note_id):
        """
        :param request: to update a note
        :param note_id: id of the note
        :return: updates the note with the new data
        """

        pdb.set_trace()

        try:
            try:

                note_object = Note.objects.get(id=note_id)

                # getting the data from request

                # getting the user

                user_id = user.id

            except Note.DoesNotExist:
                logger.error("Exception occured while accessing Note")

                self.response['message'] = "Exception occured while accessing Note"
                return self.response

            label_list = []
            collaborator_list = []
            try:

                # getting the labels from the request data

                labels = request_data['label']

                # Iterates through the labels

                for label in labels:

                    # getting the label with the given id and name
                    label_object = Label.objects.filter(user=user_id, name=label)
                    if not label_object:
                        raise Label.DoesNotExist
                    # getting the value of 'id'
                    label_id = label_object.values()[0]['id']
                    # adding each labels id to a list
                    label_list.append(label_id)
                # replacing the label data with id's list
                request_data['label'] = label_list
            except Label.DoesNotExist:
                logger.error("Exception occured while accessing Label")

                self.response['message'] = "Exception occured while accessing Label"

                return self.response
            except KeyError:
                logger.error("Key error occured")

                self.response['message'] = "Key error occured"
                return self.response

            try:

                # getting the given collaborators
                collaborators = request_data['collaborator']
                print(collaborators, "collaborators")
                # Iterates through the collaborators
                for collaborator in collaborators:
                    # getting the collaborator with the given email
                    collaborator_object = User.objects.filter(email__in=collaborators)
                    if not collaborator_object:
                        raise User.DoesNotExist
                    # getting the id of the collaborator
                    collaborator_id_list = []
                    for collab in collaborator_object:
                        collaborator_id_list.append(collab.id)
                    print(collaborator_id_list, "collaboratoridddddd")
                    # adding all the ids to the list
                    for collaborator_id in collaborator_id_list:
                        collaborator_list.append(collaborator_id)
                print("collab list : ", collaborator_list)
                request_data['collaborator'] = collaborator_list
                print("request_data : ", request_data)
            except User.DoesNotExit:
                self.response['message'] = "Exception occured while accessing the user"
                return self.response
            except KeyError:
                self.response['message'] = "KeyError occured"
                return self.response

            # makes 'partial' as 'True' because we are not using all the fileds of the Note
            serializer = NoteSerializer(note_object, data=request_data, partial=True)
            print("serailizer : ", serializer)
            print("valid serializer : ", serializer.is_valid())
            if serializer.is_valid():
                print("valid serializer")
                update_note = serializer.save()
                string_user_id = str(user.id)
                redisobject.hmset(string_user_id + "note", {update_note.id: str(json.dumps(serializer.data))})
                logger.info("Update Operation Successful")
                self.response['success'] = True
                self.response['message'] = "Update Operation Successful"
                self.response['data'].append(request_data)
                return self.response
        except Exception as e:
            print("Exception : ", e)
            self.response['message'] = "Update operation failed"
            return self.response

    # Function to delete the note

    def delete_note(self, user, note_id):
        """
        :param request: for deleting note
        :param note_id: id of the note
        :return: makes is_trash to True
        """

        try:

            # getting the note with the given id
            note = Note.objects.get(id=note_id, user_id=user.id)
            # making 'is_delete' to access it from Trash
            note.is_trash = True
            note.save()

            logger.info("Delete Operation Successful")
            self.response['success'] = True
            self.response['message'] = "Delete Operation Successful"
            self.response['data'].append(note_id)

        except Note.DoesNotExist:
            logger.error("Delete Operation Failed")
            self.response['message'] = "Delete Operation Failed"
            return self.response

        except Exception as e:
            logger.error("Delete Operation Failed")

            self.response['message'] = "Delete operation failed"
            return self.response
        return self.response

    def reminder_notification(self):

        notes_set = Note.objects.filter(reminder__isnull=False)
        print("notes set : ", notes_set)
        reminder_list = []
        initial_time = timezone.localtime(timezone.now())
        end_time = timezone.now() + timezone.timedelta(minutes=1)

        for i in range(len(notes_set)):
            print(notes_set.values()[i]['reminder'])
            if initial_time < notes_set.values()[i]['reminder'] < end_time:
                subject = "Note Reminder"
                message = render_to_string('note_reminder_email.html')
                sender = os.getenv('EMAIL_HOST_USER')
                reciever = os.getenv('EMAILID')

                send_mail(subject, message, sender, [reciever])
        self.response['success'] = True
        self.response['message'] = "Success"
        return self.response

    def get_reminders(self, user):

        try:
            user_id = user.id
            noteobjects = Note.objects.filter(user_id=user_id)

            remaining_list = []
            completed_list = []
            for noteobject in noteobjects:

                if getattr(noteobject, 'reminder') > timezone.now():
                    remaining_list.append(noteobject.reminder)
                else:
                    completed_list.append(noteobject.reminder)
            reminders = {
                "remaining": remaining_list,
                "completed": completed_list
            }
            reminder_string = str(reminders)

            response = self.smd_response(True, "Reminder operation successful", reminder_string)


        except Note.DoesNotExist:
            response = self.smd_response(False, "Exception occured while accessing the note", '')
            return response

        return response

    def get_trash(self, user):

        try:
            user_id = user.id
            noteobject = Note.objects.filter(user_id=user_id, is_trash=True)
            notevalues_str = str(noteobject.values())
        except Note.DoesNotExist:
            response = self.smd_response(False, "Exception occured while accessing note", '')
            return response
        response = self.smd_response(True, "Trash Get operation successful", notevalues_str)
        return response

    def get_archieved_notes(self, user):

        try:
            user_id = user.id
            noteobject = Note.objects.filter(user_id=user_id, is_archieve=True)
            string_note = str(noteobject.values())

        except Note.DoesNotExist:
            self.response['message'] = "Exception occured while accessing note"
            response = self.smd_response(False, "Exception occured while accessing note", '')
            return response

        response = self.smd_response(False, "Trash Get operation successful", string_note)
        return response

    def update_coll(self, user_id, request_data, note_object):
        # pdb.set_trace()

        try:

            # getting the given collaborators
            collaborators = request_data['collaborator']
            print(collaborators, "collaborators")
            collaborator_object = User.objects.filter(email__in=collaborators)
            collaborator_id_list=[]
            new_collaborator_id_list = []
            each_new_collaborator = ''
            print("note object : ",note_object)
            new_collaborator_object = note_object.collaborator
            coll_list = list(new_collaborator_object.values_list())
            print("collaborator values list : ",coll_list)
            coll_list_length = len(coll_list)
            print("collaborator values list length : ",coll_list_length)
            old_collaborator_list = []
            for i in range(coll_list_length):
                old_collaborator = note_object.collaborator.values()[i]['email']
                old_collaborator_list.append(old_collaborator)
            print("Old collaborator list : ",old_collaborator_list)
            old_collaborator_id_list = []

            each_old_collaborator = ''
            for each_old_collaborator in old_collaborator_list:
                user_object = User.objects.get(email=each_old_collaborator)
                collaborator_id = user_object.id
                old_collaborator_id_list.append(collaborator_id)
            print("old collaborator id  list : ",old_collaborator_id_list)
            for each_new_collaborator in collaborator_object:
                new_collaborator_id_list.append(each_new_collaborator.id)
            print("new collaborator id list : ",new_collaborator_id_list)
            total_list_length = len(old_collaborator_id_list)+len(new_collaborator_id_list)
            final_collaborator_list = old_collaborator_id_list+new_collaborator_id_list
            final_collaborator_list_without_duplicates = list(dict.fromkeys(final_collaborator_list))
            print("final collaborator list : ",final_collaborator_list)
            print("final collaborator list without duplicates : ",final_collaborator_list_without_duplicates)
            request_data['collaborator'] = final_collaborator_list_without_duplicates
            print("request_data : ", request_data)
        except User.DoesNotExist:
            self.response['message'] = "Exception occured while accessing the user"
            return self.response
        except KeyError:
            self.response['message'] = "KeyError occured"
            return self.response

        # makes 'partial' as 'True' because we are not using all the fileds of the Note
        serializer = NoteSerializer(note_object, data=request_data, partial=True)
        if serializer.is_valid():
            update_note = serializer.save()
            string_user_id = str(user_id)
            redisobject.hmset(string_user_id + "note", {update_note.id: str(json.dumps(serializer.data))})
            logger.info("Update Operation Successful")
            self.response['success'] = True
            self.response['message'] = "Update Operation Successful"
            self.response['data'].append(request_data)
            return self.response
