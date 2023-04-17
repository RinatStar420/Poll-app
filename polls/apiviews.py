from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Poll, Choice
from .api.serializers import PollSerializer, ChoiceSerializer, VoteSerializer, UserSerializer
from django.contrib.auth import authenticate


# Используйте viewsets.ModelViewSet, когда вы собираетесь разрешить все или большинство операций CRUD над моделью.
# Используйте generics.*, если вы хотите разрешить только некоторые операции над моделью.
# Используйте APIView, когда вы хотите полностью настроить параметры поведения.


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    """Для URL /polls/ и /polls/<pk>/ требуется два класса представлений с одинаковым 
сериализатором ибазовым набором queryset. Мы можем сгруппировать их в набор  
представлений и соединить их с урлами с помощью маршрутизатора."""


# class PollList(generics.ListCreateAPIView):
#     queryset = Poll.objects.all()
#     serializer_class = PollSerializer
#
#
# class PollDetail(generics.RetrieveDestroyAPIView):
#     queryset = Poll.objects.all()
#     serializer_class = PollSerializer


class ChoiceList(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id=self.kwargs['pk'])
        return queryset

    serializer_class = ChoiceSerializer


class CreateVote(APIView):
    serializer_class = VoteSerializer

    def post(self, request, pk, choice_pk):
        voted_by = request.data.get("voted_by")
        data = {'choice': choice_pk, 'poll': pk, 'voted_by': voted_by}
        serializer = VoteSerializer(data=data)

        if serializer.is_valid():
            vote = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = ()

    def post(self, request, ):
        username = request.get('username')
        password = request.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response({'token': user.auth_token.key})
        else:
            return Response({'error': 'Wrong Credentials'}, status=status.HTTP_400_BAD_REQUEST)
