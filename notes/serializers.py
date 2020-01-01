from rest_framework import serializers
from .models import Img, Note, Label


class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Img
        fields = ['imgs']


class NoteShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['title', 'note']


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['title', 'note', 'label', 'collaborator', 'image', 'is_archieve', 'is_trash', 'reminder', 'is_pin', 'url']


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name']
class NotesSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['title']

class CollaboratorSearializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['title','collaborator']