from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, OpenApiResponse

from django.http import HttpResponse
from django.urls import reverse

from .models import Salon
from .mongo_utils import save_picture_to_mongodb, get_picture_from_mongodb, delete_picture_from_mongodb
from .serializers import SalonSerializer, SalonUpdateSerializer


@extend_schema(
    summary='Create a new salon',
    description='Create a new salon with details including a picture.',
    request=SalonSerializer,
    responses={
        201: OpenApiResponse(description='Salon created successfully', examples={
            'application/json': {
                'message': 'Salon created successfully',
                'image_url': 'http://example.com/path/to/image',
                'picture_id': '60d5ec49e7e43b39e76c9d7c',
                'salon_id': 1
            }
        }),
        400: OpenApiResponse(description='Invalid input data')
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_salon(request):
    serializer = SalonSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        # serializer.validated_data['user'] = request.user

        salon = serializer.save()
        picture_data = request.data.get('picture').read() if 'picture' in request.data else None
        picture_id = save_picture_to_mongodb(picture_data)
        
        salon.pic_id = str(picture_id)
        salon.save()
        image_url = request.build_absolute_uri(reverse('serve_image', args=[salon.pic_id]))
        
        return Response({
            'message': 'Salon created successfully',
            'image_url': image_url,
            'picture_id': str(picture_id),
            'salon_id': salon.id
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary='Retrieve a specific salon',
    description='Retrieve details of a specific salon by its ID.',
    responses={
        200: SalonSerializer,
        404: OpenApiResponse(description='Salon not found')
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_salon(request, salon_id):
    try:
        salon = Salon.objects.get(id=salon_id)
        serializer = SalonSerializer(salon, context={'request': request})
        return Response(serializer.data)

    except Salon.DoesNotExist:
        return Response({
            'error': 'Salon not found'
        }, status=404)
    

@extend_schema(
    summary='Retrieve all salons',
    description='Retrieve details of all salons.',
    responses={
        200: SalonSerializer(many=True)
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_salons(request):
    salon = Salon.objects.all()
    serializer = SalonSerializer(salon, many=True, context={'request': request})
    return Response(serializer.data)


@extend_schema(
    summary='Retrieve salons created by the authenticated user',
    description='Retrieve details of all salons created by the authenticated user.',
    responses={
        200: SalonSerializer(many=True)
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_user_salons(request):
    salon = Salon.objects.filter(user=request.user)
    serializer = SalonSerializer(salon, many=True, context={'request': request})
    return Response(serializer.data)


@extend_schema(
    summary='Update a salon',
    description='Update details of a specific salon by its ID. Only the fields provided in the request will be updated.',
    request=SalonUpdateSerializer,
    responses={
        200: OpenApiResponse(description='Salon updated successfully'),
        400: OpenApiResponse(description='Invalid input data'),
        404: OpenApiResponse(description='Salon not found')
    }
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_salon(request, salon_id):
    try:
        salon = Salon.objects.get(id=salon_id)
        serializer = SalonUpdateSerializer(salon, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Salon updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Salon.DoesNotExist:
        return Response({'error': 'Salon not found'}, status=status.HTTP_404_NOT_FOUND)



@extend_schema(
    summary='Delete a salon',
    description='Delete a specific salon by its ID. If the salon has an associated picture, it will be deleted from the database.',
    responses={
        204: OpenApiResponse(description='Salon deleted successfully'),
        404: OpenApiResponse(description='Salon not found')
    }
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_salon(request, salon_id):
    try:
        salon = Salon.objects.get(id=salon_id)
        
        pic_id = salon.pic_id
    
        if pic_id and len(pic_id) > 5:
            delete_picture_from_mongodb(pic_id)
            
        salon.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    except Salon.DoesNotExist:
        return Response({'error': 'Salon not found'}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    summary='Serve an image',
    description='Serve an image associated with a specific salon by its ID.',
    responses={
        200: OpenApiResponse(description='Image retrieved successfully'),
        404: OpenApiResponse(description='Image not found')
    }
)
def serve_image(request, salon_id):
    picture_data = get_picture_from_mongodb(salon_id)

    if picture_data:
        response = HttpResponse(picture_data, content_type='image/jpeg')
        return response
    else:
        return HttpResponse(status=404)
    