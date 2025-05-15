from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser  # Para manejar archivos
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token

from .models import (
    Usuario, Rol, PeriodoAcademico, Planificacion,
    Actividad, DetalleActividad, Evidencia, Notificacion
)

from .serializers import (
    UsuarioSerializer, RolSerializer, PeriodoAcademicoSerializer,
    PlanificacionSerializer, ActividadSerializer,
    DetalleActividadSerializer, EvidenciaSerializer,
    NotificacionSerializer, CustomAuthTokenSerializer
)

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer

class PeriodoAcademicoViewSet(viewsets.ModelViewSet):
    queryset = PeriodoAcademico.objects.all()
    serializer_class = PeriodoAcademicoSerializer

class PlanificacionViewSet(viewsets.ModelViewSet):
    serializer_class = PlanificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.roles.filter(nombre='decano').exists():
            return Planificacion.objects.all()
        else:
            return Planificacion.objects.filter(usuario=user)

class ActividadViewSet(viewsets.ModelViewSet):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer

class DetalleActividadViewSet(viewsets.ModelViewSet):
    serializer_class = DetalleActividadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.roles.filter(nombre='decano').exists():
            return DetalleActividad.objects.all()
        else:
            return DetalleActividad.objects.filter(planificacion__usuario=user)

class EvidenciaViewSet(viewsets.ModelViewSet):
    serializer_class = EvidenciaSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # Para manejar archivos

    def get_queryset(self):
        user = self.request.user
        if user.roles.filter(nombre='decano').exists():
            return Evidencia.objects.all()
        else:
            return Evidencia.objects.filter(detalle_actividad__planificacion__usuario=user)
        
    def perform_create(self, serializer):
        # Esto guarda el archivo subido
        serializer.save()

class NotificacionViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.roles.filter(nombre='decano').exists():
            return Notificacion.objects.all()
        else:
            return Notificacion.objects.filter(usuario=user)

class ObtainAuthToken(APIView):
    permission_classes = [AllowAny] # Permitimos accesso sin autenticación

    def post(self, request, *args, **kwargs):
        serializer = CustomAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vista_protegida(request):
    """
    Vista protegida que solo puede ser accedida por usuarios autenticados.
    """
    return Response({
        "mensaje": f"¡Hola, {request.user.username}! Estás autenticado correctamente.",
        "usuario_id": request.user.id,
        "email": request.user.email,
        })