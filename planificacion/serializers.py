from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import (
    Usuario, Rol, PeriodoAcademico, Planificacion,
    Actividad, DetalleActividad, Evidencia, Notificacion
)

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        roles_data = validated_data.pop('roles', [])
        password = validated_data.pop('password')
        usuario = Usuario(**validated_data)
        usuario.set_password(password)  # esto genera el hash
        usuario.save()
        usuario.roles.set(roles_data)
        return usuario
    
class CustomAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        # Validación de dominio, solo usuarios de @yachaytech.edu.ec
        if not username.endswith('@yachaytech.edu.ec'):
            raise serializers.ValidationError("Correo no permitido. Dirección de dominio no válida.")
        
        # Autenticación con correo
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Credenciales incorrectas.")
        return user

class PeriodoAcademicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodoAcademico
        fields = '__all__'

class PlanificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planificacion
        fields = '__all__'

class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = '__all__'

class DetalleActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleActividad
        fields = '__all__'

class EvidenciaSerializer(serializers.ModelSerializer):
    # Usamos FileField para permitir la subida de archivos
    nombre_archivo = serializers.FileField() # Archivo real
    url_archivo = serializers.URLField(required=False) # URL opcional
    class Meta:
        model = Evidencia
        fields = '__all__'

class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = '__all__'