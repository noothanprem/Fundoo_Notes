import pdb

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from notes.models import Label
import json
import logging
from fundoo.settings import file_handler
from notes.lib.redis_function import RedisOperation
from utility import Response

response_class_object = Response()
redisobject = RedisOperation()


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
print(file_handler,"file")


class LabelOperations:
    redisobject.__connect__()


    def create_label(self, request):
        """

        :param request: to create label
        :return: creates label
        """

        try:
            name = request.data['name']

            user = request.user
            user_id = user.id

            #getting the user with the given id
            userobject = User.objects.get(id=user.id)

            if Label.objects.filter(user_id=user_id, name=name).exists():

                response = self.smd_response(False, "Label already exists", '')
                return response
            labelobject = Label.objects.create(name=name, user=userobject)

            string_userid = str(user_id)
            redisobject.hmset(string_userid + "label", {labelobject.id: name})
            logger.info("note is created")

            response = response_class_object.smd_response(True,"Label created successfully",'')
            logger.info("Label created successfully")
        except Label.DoesNotExist:
            logger.info("Exception occured while accessing the user")
            response = response_class_object.smd_response(False, "Exception occured while accessing the Label", '')

        return response


    def get_label(self, request):
        """

        :param request:get the labels of the user
        :return: returns all the labels of that particular user
        """

        global label_name
        try:

            user = request.user
            string_userid = str(user.id)
            userlabels = redisobject.hvals(string_userid + "label")
            userlabelsstring = str(userlabels)
            print(userlabels, "from redisssss")

            if userlabels is None:
                labels = Label.objects.filter(user_id=user.id)
                userlabelsstring = [i.name for i in labels]
                logger.info("labels where fetched from database for user :%s", request.user)
            logger.info("labels where fetched from redis")
            response = response_class_object.smd_response(True, "Read Operation Successfull", userlabelsstring)
        except Label.DoesNotExist:
            logger.info("Exception occured while getting the Label")
            response = response_class_object.smd_response(False, "Exception occured while getting the Label", '')
        return response

    def update_label(self, request, label_id):
        """

        :param request:to update the particular label
        :param label_id: id of the label to be updated
        :return: updates the label
        """

        try:


            user = request.user
            request_body = request.body
            body_unicode = request_body.decode('utf-8')
            body_unicode_dict = json.loads(body_unicode)
            user_id = user.id

            label_object = Label.objects.get(id=label_id, user_id=user_id)

            name=body_unicode_dict['name']
            label_object.name =name

            label_object.save()
            string_user_id = str(user.id)
            redisobject.hmset(string_user_id + "label", {label_object.id: label_id})

            logger.info("Label Updated Successfully")
            response = response_class_object.smd_response(True, "Label Updated Successfully", '')

        except Label.DoesNotExist:
            logger.error("Exception occured while getting the Label object")
            response = response_class_object.smd_response(False, "Exception occured while getting the Label object", '')

        except Exception:
            logger.error("Exception occured")
            response = response_class_object.smd_response(False, "Exception", '')

        return response

    def delete_label(self, request, label_id):
        """

        :param request: to delete the particular label
        :param label_id: id of the label to be deleted
        :return: deletes the given label
        """

        try:
            # pdb.set_trace()

            user = request.user
            user_id = user.id

            label_object = Label.objects.get(id=label_id, user_id=user_id)

            label_object.delete()
            string_user_id = str(user_id)
            redisobject.hdel(string_user_id + "label", label_id)
            logger.info("Label Deleted Successfully")
            response = response_class_object.smd_response(True, "Label Deleted Successfully", '')
        except Label.DoesNotExist:
            logger.error("Exception occured while getting the Label object")
            response = response_class_object.smd_response(False, "Exception occured while getting the Label object", '')
        except Exception:
            logger.error("Exception Occured")
            response = response_class_object.smd_response(False, "Exception occured", '')
        return response
