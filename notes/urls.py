from django.urls import path,include
from django.conf.urls import url
from . import views
from .background_tasks import hello


urlpatterns=[
    path('upload_image',views.UploadImage.as_view(), name='upload_view'),
    path('note_share',views.NoteShare.as_view(), name='noteshare_view'),
    path('notes',views.CreateNote.as_view(), name='createnote_view'),
    path('labels',views.CreateLabel.as_view(), name='createlabel_view'),
    path('labels/<label_id>',views.UpdateLabel.as_view(), name='updatelabel_view'),
    path('notes/<note_id>',views.UpdateNote.as_view(), name='updatenote_view'),
    path('notes_trash',views.Trash.as_view(),name='trashview'),
    path('notes_archieve',views.Archieve.as_view(), name="archieveview"),
    path('notes_reminder',views.Reminder.as_view(), name="reminderview"),
    path('image_loading',views.ImageLoading.as_view(),name='imageloading'),
    path('reminder_notification',views.ReminderNotification.as_view(),name='remindernotification'),
    path('search/<query_data>',views.NotesSearch.as_view(),name='searchview'),
    path('background_task',views.BackgroundTasks.as_view(),name='background_task_view')
]

hello(repeat=5,repeat_until=None)