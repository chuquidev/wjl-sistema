from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Usuario
from .serializers import (
    UsuarioListSerializer,
    UsuarioCrearSerializer,
    UsuarioActualizarSerializer,
    CambiarPasswordSerializer,
    PerfilSerializer,
)

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import TokenPorCorreoSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.select_related('sucursal').filter(activo=True)
    filter_backends  = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['rol', 'sucursal']
    search_fields    = ['correo', 'nombres', 'apellidos', 'dni']
    ordering_fields  = ['apellidos', 'nombres', 'creado_en']

    def get_serializer_class(self):
        if self.action == 'create':
            return UsuarioCrearSerializer
        if self.action in ['update', 'partial_update']:
            return UsuarioActualizarSerializer
        return UsuarioListSerializer

    # ── Ver y editar perfil propio ────────────────────────
    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def perfil(self, request):
        if request.method == 'PATCH':
            serializer = PerfilSerializer(
                request.user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        # GET
        serializer = PerfilSerializer(request.user)
        return Response(serializer.data)

    # ── Cambiar contraseña propia ─────────────────────────
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def cambiar_password(self, request):
        serializer = CambiarPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        usuario = request.user
        if not usuario.check_password(serializer.validated_data['password_actual']):
            return Response(
                {'password_actual': ['La contraseña actual es incorrecta.']},
                status=status.HTTP_400_BAD_REQUEST
            )

        usuario.set_password(serializer.validated_data['password_nuevo'])
        usuario.save()
        return Response({'mensaje': 'Contraseña actualizada correctamente.'})

    # ── Desactivar usuario ────────────────────────────────
    @action(detail=True, methods=['post'])
    def desactivar(self, request, pk=None):
        usuario = self.get_object()
        if usuario == request.user:
            return Response(
                {'error': 'No puedes desactivarte a ti mismo.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        usuario.activo = False
        usuario.save()
        return Response({'mensaje': 'Usuario desactivado correctamente.'})


class TokenPorCorreoView(TokenObtainPairView):
    serializer_class = TokenPorCorreoSerializer