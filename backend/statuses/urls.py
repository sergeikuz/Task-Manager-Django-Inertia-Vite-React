from django.urls import path

from backend.statuses import views

app_name = 'statuses'
urlpatterns = [
    path("", views.StatusesIndexView.as_view(), name="statuses_index"),
    path(
        "create/",
        views.StatusesCreateView.as_view(),
        name="statuses_create"),
    path(
        "<int:pk>/update/",
        views.StatusesUpdateView.as_view(),
        name="statuses_update"),
    path(
        "<int:pk>/delete/",
        views.StatusesDeleteView.as_view(),
        name="statuses_delete"),
]
