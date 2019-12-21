import pdb

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import HttpResponse
from notes.models import Note, Label
from notes.lib.redis_function import RedisOperation
from notes.serializers import NoteSerializer
from fundoo.settings import file_handler
import json
import logging



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
        self.response['success']=success
        self.response['message']=message
        self.response['data']=data
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
            data = request.data # getting the user
            user = request.user
            user_id = user.id
            # creating the lists for collaborators and labels
            collab_list = []
            label_list = []
            labels = data['label'] # iterates through all the labels in the list
            for label in labels: # getting each label and adding the label_id to the list
                labelobject = Label.objects.filter(user_id=user_id, name=label)
                if not labelobject:
                    raise Label.DoesNotExist
                label_id = labelobject.values()[0]['id']
                label_list.append(label_id)
                print("label list  : ",label_list)
            #replaces the 'label' in data with the new label_list
            data['label'] = label_list
        except Label.DoesNotExist:
            logger.error("Exception occured while accessing label")
            response = self.smd_response(False,"Exception occured while accessing label",[])
            return response
        except Exception:
            logger.error("Exception occured")
            response = self.smd_response(False, "Exception occured", [])
            return self.response

        try:
            collaborators = data['collaborator']
            #getting the collaborators with the given email
            collaborator_object = User.objects.filter(email__in=collaborators)

            if not collaborator_object:
                raise User.DoesNotExist
            #getting the id of the collaborator
            collaborator_id_list=[]
            for collab in collaborator_object:
                collaborator_id_list.append(collab.id)
                print("collaborator id list : ",collaborator_id_list)
            #adding all the ids to the list
            for collaborator_id in collaborator_id_list:
                collab_list.append(collaborator_id)
                print("collaborator list : ",collab_list)

            #replaces in the data with the new list
            data['collaborator'] = collab_list
            print("data : ",data)

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

            string_user_id=str(user.id)
            redisobject.hmset(string_user_id + "note",{create_note.id: str(json.dumps(serializer.data))})

            logger.info("note created successfully")
            self.response['success']=True
            self.response['message']="note created successfully"
            self.response['data'].append(data)
            return self.response
        logger.error("note creation failed")

        response = self.smd_response(False, "Note creation failed", [])
        return response


    def get_note(self, request, note_id):
        """
        :param request: to get the note
        :param note_id: id of the note
        :return: returns the note
        """


        try:

            user = request.user
            string_user_id=str(user.id)
            redis_data=redisobject.hvals(string_user_id+"note")
            str_note_data=str(redis_data)

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



    def update_note(self, request, note_id):
        """
        :param request: to update a note
        :param note_id: id of the note
        :return: updates the note with the new data
        """


        try:
            try:

                note_object = Note.objects.get(id=note_id)

                #getting the data from request

                request_data = request.data


                #getting the user

                user = request.user


                user_id = request.user.id

            except Note.DoesNotExist:
                logger.error("Exception occured while accessing Note")

                self.response['message'] = "Exception occured while accessing Note"
                return self.response

            label_list = []
            collaborator_list = []
            try:

                #getting the labels from the request data

                labels = request_data['label']

                #Iterates through the labels

                for label in labels:

                    #getting the label with the given id and name
                    label_object = Label.objects.filter(user=user_id, name=label)
                    if not label_object:
                        raise Label.DoesNotExist
                    #getting the value of 'id'
                    label_id = label_object.values()[0]['id']
                    #adding each labels id to a list
                    label_list.append(label_id)
                #replacing the label data with id's list
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

                #getting the given collaborators
                collaborators = request_data['collaborator']
                print (collaborators, "collaborators")
                #Iterates through the collaborators
                for collaborator in collaborators:
                    #getting the collaborator with the given email
                    collab_list=[]
                    collaborator_object = User.objects.filter(email__in=collaborators)
                    if not collaborator_object:
                        raise User.DoesNotExist
                    #getting the id of the collaborator
                    collaborator_id_list = []
                    for collab in collaborator_object:
                        collaborator_id_list.append(collab.id)
                    print(collaborator_id_list, "collaboratoridddddd")
                    #adding all the ids to the list
                    for collaborator_id in collaborator_id_list:
                        collab_list.append(collaborator_id)

                request_data['collab'] = collaborator_list
            except User.DoesNotExit:
                self.response['message']="Exception occured while accessing the user"
                return self.response
            except KeyError:
                self.response['message']="KeyError occured"
                return self.response

            #makes 'partial' as 'True' because we are not using all the fileds of the Note
            serializer = NoteSerializer(note_object, data=request_data, partial=True)

            if serializer.is_valid():
                update_note = serializer.save()
                string_user_id=str(user.id)
                redisobject.hmset(string_user_id + "note",{update_note.id: str(json.dumps(serializer.data))})
                logger.info("Update Operation Successful")
                self.response['success'] = True
                self.response['message'] = "Update Operation Successful"
                self.response['data'].append(request_data)
                return self.response
        except Exception:
            self.response['message']="Update operation failed"
            return self.response

    #Function to delete the note

    def delete_note(self, request, note_id):
        """
        :param request: for deleting note
        :param note_id: id of the note
        :return: makes is_trash to True
        """

        #pdb.set_trace()
        user = request.user
        try:

            #getting the note with the given id
            note = Note.objects.get(id=note_id, user_id=user.id)
            #making 'is_delete' to access it from Trash
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
