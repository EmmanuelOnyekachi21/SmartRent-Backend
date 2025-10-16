from account.serializers import AccountProfileReadSerializer
from rest_framework.decorators import api_view
from account.models import Account
from rest_framework.response import Response

@api_view(['GET'])
def get_users(request):
    if request.method == "GET":
        users = Account.objects.all()
        serializer = AccountProfileReadSerializer(users, many=True)
        return Response(serializer.data)