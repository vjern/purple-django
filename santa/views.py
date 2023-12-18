from django.shortcuts import render
from django.urls import path

# Create your views here.
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter

from .models import User, Exclusion
from .serializers import UserSerializer, ExclusionSerializer
from .core.draw import draw


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


router = DefaultRouter()
router.register('users', UserViewSet)


def index(request):
    return HttpResponse("Hello, world. You're at the santa index.")


# GET /draw
def new_draw():
    # no input data, only use what's in the db
    # fetch data
    users = [u.id for u in User.objects.all()]
    exclusions = {}
    # compute draw
    draw_data: list[tuple[int, int]] = draw(users, exclusions)
    return {
        'pairs': draw_data,
    }


# GET /history
def get_draw_history(n: int = 5):
    # `n` as a query param
    f"""
    SELECT *
    FROM draw_history
    WHERE draw IN (
        SELECT id FROM draw
        ORDER BY timestamp
        LIMIT {n}
    )
    """
    # then squash it into a list of lists

urlpatterns = [
    *router.urls,
    # path(
    #     r'^users/$',
    #     UserViews.ListCreate.as_view(),
    #     name='user-list',
    # ),
    # url(
    #     r'^mymodels/(?P<pk>[^/.]+)/$',
    #     UserViews.RetrieveUpdateDestroy.as_view(),
    #     name='user-detail',
    # ),
    # url(
    #     r'^mymodels/custom_action/$',
    #     MyModelCustomActionAPIView.as_view(),
    #     name='mymodel-custom-action',
    # ),
]
print(__file__, f"{urlpatterns = }")