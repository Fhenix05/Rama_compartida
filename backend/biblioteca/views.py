from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
from datetime import datetime, timedelta
import jwt
from django.db.models import Q  # Para agilizar el filtrado
from .models import Libro, Categoria, Usuario
from .serializers import (
    RegistroSerializer, LoginSerializer, UsuarioSerializer,
    LibroSerializer, CategoriaSerializer
)


class RegistroView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Usuario registrado correctamente'}, status=201)
        return Response(serializer.errors, status=400)

class ListarUsuariosView(APIView):
    def get(self, request):
        usuarios = Usuario.objects.filter(is_active=True)
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.validated_data['usuario']
            #Validacion en el login
            if not usuario.is_active:
                return Response({'error': 'Usuario desactivado'}, status=403)
            
            payload = {
                'usuario_id':  usuario.usuario_id,
                
                'exp': datetime.utcnow() + timedelta(hours=8),
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            return Response({
                'token':   token,
                'usuario': UsuarioSerializer(usuario).data
            })
        return Response(serializer.errors, status=400)


# Sin verificación de token por ahora xdxd
class LibrosView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        busqueda  = request.query_params.get('busqueda', '')
        categoria = request.query_params.get('categoria', '')

        libros = Libro.objects.all()

        if busqueda:
            libros = libros.filter(
                Q(libro_titulo__icontains=busqueda) | 
                Q(libro_autor__icontains=busqueda)
            )

        if categoria:
            libros = libros.filter(categoria__categoria_id=categoria)

        serializer = LibroSerializer(libros, many=True)
        return Response(serializer.data)


class CategoriasView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)