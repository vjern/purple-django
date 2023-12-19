from collections import defaultdict

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

    def list(self, request):
        """
        List contents of table `draw`.
        Optional query param `latest` (int) allows to retrieve only the n latest
        draws.
        """
        queryset = Draw.objects.all()
        # Parse `latest` query param
        latest = request.query_params.get('latest', 0)
        try:
            latest = int(latest)
        except ValueError:
            return HttpResponse("'latest' query param must be an integer", status=400)
        if latest:
            queryset = queryset.order_by('-timestamp')[:latest]
        #
        return JsonResponse(
            data=DrawSerializer(queryset, many=True).data,
            status=200,
            safe=False,
        )

    def create(self, validated_data):
        """
        Create a draw from the DB's contents. No input data is required.
        Add the draw and its pairs to the DB.
        """
        try:
            draw, pairs = new_draw()
        except RuntimeError as err:
            return HttpResponse(err.args[0], status=500)
        data = DrawSerializer(draw).data
        data['pairs'] = [
            {'giver': giver, 'taker': taker}
            for giver, taker in pairs
        ]
        return JsonResponse(data=data, status=200)

    def retrieve(self, request, *, pk):
        """
        We extend the default behavior of `ModelViewSet.retrieve` to retrieve
        the list of pairs as well as the draw object metadata.
        This is the only way to retrieve the full data of a draw object.
        """
        response = super().retrieve(request, pk=pk)
        draw = Draw(id=pk)
        response.data['pairs'] = [
            {'giver': pair.giver.id, 'taker': pair.taker.id}
            for pair in DrawPair.objects.filter(draw=draw)
        ]
        return response


def liveness(request):
    """Simple liveness endpoint."""
    return HttpResponse("secret-santa 1.0.0")


def new_draw() -> tuple[Draw, list[DrawPair]]:
    """
    Compute a new draw from the DB users & exclusions between users
    and save it to the DB.
    """
    # fetch data
    users: list[int] = [u.id for u in User.objects.all()]
    exclusions: dict[int, set[int]] = defaultdict(set)
    for exc in Exclusion.objects.all():
        exclusions[exc.recipient.id].add(exc.target.id)
    # compute new santa draw
    pairs: list[tuple[int, int]] = generate_draw(users, exclusions)
    # Register it
    draw = Draw()
    draw.save()
    # Then register draw pairs
    for giver_id, taker_id in pairs:
        DrawPair(
            draw=draw,
            giver=User(id=giver_id),
            taker=User(id=taker_id),
        ).save()
    return draw, pairs


router = DefaultRouter()
router.register('users', UserViewSet)
router.register('exclusions', ExclusionViewSet)
router.register('draws', DrawViewSet)
