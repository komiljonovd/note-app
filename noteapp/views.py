from rest_framework.viewsets import ModelViewSet,generics
from rest_framework.permissions import IsAuthenticated
from .models import Document,DocumentAccess
from .serializers import DocumentSerializer,DocumentAccessSerializer
from rest_framework.response import Response

class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DocumentAccessViewSet(ModelViewSet):
    queryset = DocumentAccess.objects.all()
    serializer_class = DocumentAccessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            DocumentAccess.objects.filter(document__owner=self.request.user) |
            DocumentAccess.objects.filter(user=self.request.user)
        ).distinct()


    def create(self, request, *args, **kwargs):
        document_id = request.data.get('document')
        user_id = request.data.get('user')

        

        if not document_id or not user_id:
            return Response({'error': 'document and user required'}, status=400)

        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            return Response({'error': 'Document not found'}, status=404)

        # ✅ только owner может добавлять
        if document.owner != request.user:
            return Response({'error': 'Only owner can add users'}, status=403)

        # ❗ нельзя добавить себя
        if int(user_id) == request.user.id:
            return Response({'error': 'You are owner'}, status=400)

        # ❗ проверка дубликата
        if DocumentAccess.objects.filter(document=document, user_id=user_id).exists():
            return Response({'error': 'User already added'}, status=400)

        access = DocumentAccess.objects.create(
            document=document,
            user_id=user_id
        )

        serializer = self.get_serializer(access)
        return Response(serializer.data, status=201)
    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # ✅ только owner документа может удалить
        if instance.document.owner != request.user:
            return Response({'error': 'Only owner can remove users'}, status=403)

        instance.delete()
        return Response({'status': 'deleted'}, status=204)
