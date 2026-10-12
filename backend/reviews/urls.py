from django.urls import path
from .views import ReviewListView, ReviewCreateView, ReviewHelpfulVoteView

urlpatterns = [
    path('', ReviewListView.as_view(), name='review-list'),
    path('create/', ReviewCreateView.as_view(), name='review-create'),
    path('<int:pk>/vote/', ReviewHelpfulVoteView.as_view(), name='review-vote'),
]
