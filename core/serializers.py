from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer,\
    UserSerializer as BaseUserSerializer


class UserCreateSerializer(BaseUserCreateSerializer):
    # That class will inherit all the features of the BaseUserCreateSerializer that we want to add in it
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
