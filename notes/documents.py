from django_elasticsearch_dsl import Index,fields,Document
from django_elasticsearch_dsl.registries import registry
from .models import Note
from elasticsearch_dsl import analyzer, tokenizer

html_strip = analyzer('html_strip',
    tokenizer="edge_ngram",
    filter=["lowercase", "stop", "snowball"]
)

@registry.register_document
class NotesDocument(Document):

    title = fields.TextField(analyzer=html_strip)
    note = fields.TextField(analyzer=html_strip)
    reminder = fields.TextField()
    color = fields.TextField(analyzer=html_strip)
    label = fields.ObjectField(
        properties = {
            'name':fields.TextField(analyzer=html_strip)
        }
    )

    class Index:
        #Name of the Elasticsearch index
        name = 'note_index'
        #See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
        'number_of_replicas': 0}



    class Django:
        model = Note

        #The fields of the model you want to be indexed in Elasticsearch


        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True

        # Don't perform an index refresh after every update (overrides global setting):
        # auto_refresh = False

        # Paginate the django queryset used to populate the index with the specified size
        # (by default it uses the database driver's default setting)
        # queryset_pagination = 5000