from django.shortcuts import render
from django.urls import path

# Create your views here.
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter

from .models import User, Exclusion, Draw, DrawPair
from .serializers import UserSerializer, ExclusionSerializer, DrawSerializer
from .core.draw import generate_draw


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ExclusionViewSet(viewsets.ModelViewSet):
    queryset = Exclusion.objects.all()
    serializer_class = ExclusionSerializer


class DrawViewSet(viewsets.ModelViewSet):
    queryset = Draw.objects.all()
    serializer_class = DrawSerializer

    def create(self, validated_data):
        try:
            draw = new_draw()
        except RuntimeError as err:
            return HttpResponse(err.args[0], status=500)
        return JsonResponse(data=DrawSerializer(draw).data, status=200)


router = DefaultRouter()
router.register('users', UserViewSet)
router.register('exclusions', ExclusionViewSet)
router.register('draws', DrawViewSet)


def index(request):
    return HttpResponse("Hello, world. You're at the santa index.")


def new_draw():
    # fetch data
    users = [u.id for u in User.objects.all()]
    exclusions = defaultdict(set)
    for exc in Exclusion.objects.all():
        exclusions[exc.recipient.id].add(exc.target.id)
    # compute new santa draw
    pairs = generate_draw(users, exclusions)
    # Register it
    draw = Draw()
    draw.save()
    # Then register draw pairs
    for giver_id, taker_id in pairs:
        DrawPair(
            draw=draw,
            giver=User(id=giver_id),
            taker=User(id=taker_id)
        ).save()
    return draw


# GET /history
def get_draw_history(request, n: int = 5):
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