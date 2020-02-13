from drf_rw_serializers import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.files import File
from django.http import HttpResponse
from .models import *
from .serializers import *


class LearndataViewSet(ModelViewSet):
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return LearndataReadSerializer
        return LearndataSerializer

    def get_queryset(self):
        user = self.request.user
        return Learndata.objects.filter(subject__user__id=user.id)


class NotesViewSet(ModelViewSet):
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return NoteReadSerializer
        return NoteSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Note.objects.filter(subject__user__id=user.id)

        params = self.request.query_params
        search_q = params.get('search', None)
        filter_subjects = params.get('subjects', None)
        sort_q = params.get('order', None)

        if search_q:
            queryset = queryset.filter(content__contains=search_q)

        if filter_subjects:
            subject_uuids = [ uuid.strip() for uuid in filter_subjects.split(',') ]
            queryset = queryset.filter(subject__uuid__in=subject_uuids)
            
        if sort_q:
            queryset = queryset.order_by(sort_q) # Yes, this *is* SQL-injections-safe. Thanks Django!

        return queryset

    @action(methods=['get', 'post'], detail=True)
    def convert(self, request, uuid_or_in_format, out_format):
        import pypandoc, uuid, os
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        from base64 import b64encode
        """
        /notes/convert/:uuid_or_in_format/:out_format
        """

        IN_FORMATS = 'pdf tex docx txt odt markdown asciidoc rst epub mediawiki'.split(' ')
        OUT_FORMATS = [ f for f in IN_FORMATS if f not in 'pdf docx'.split(' ') ]

        PANDOC_FORMATS = {
            'markdown': 'markdown_phpextra+emoji+superscript+subscript',
            'tex': 'latex',
            'txt': 'plain'
        }
        FILE_ONLY_FORMATS = ('docx', 'odt', 'pdf')

        MIME_TYPES = {
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'pdf': 'application/pdf',
            'odt': 'application/vnd.oasis.opendocument.text'
        }

        if uuid_or_in_format in IN_FORMATS:
            in_format = uuid_or_in_format
            content = request.data['content']
            title = request.data['title']
        else:
            from learn.models import Note
            note = Note.objects.get(uuid=uuid_or_in_format, subject__user__id=request.user.id)
            #FIXME: ugly code. explanation: somehow, note.format contains a (actual, verbose) tuple, but as a _string_ repr.
            in_format = note.format.replace('(','').split(' ')[0].replace(',','').replace("'",'').lower()
            content = note.content
            title = note.name
        
        pandoc_in = PANDOC_FORMATS.get(in_format, in_format)
        pandoc_out = PANDOC_FORMATS.get(out_format, out_format)
        
        print(f"Converting w/ pandoc: {pandoc_in} ~> {pandoc_out}")
        
        if pandoc_out in FILE_ONLY_FORMATS:
            filename = f'temp-{uuid.uuid4()}'
            default_storage.save(filename, ContentFile(
                f'<head><title>{title}</title></head><body>{content}</body>'
            ))
            converted_filename = filename+'-converted.'+pandoc_out
            pandoc_args = tuple()
            if pandoc_out == 'pdf':
                css_filepath = default_storage.open('css_resources/pandoc.css').name
                pandoc_out = 'html5'
                pandoc_args=(
                    '--standalone',
                    '--pdf-engine', 'wkhtmltopdf',
                    '-c', css_filepath,
                )
            
            pypandoc.convert_file(
                default_storage.open(filename).name,
                format=pandoc_in,
                to=pandoc_out,
                outputfile=converted_filename,
                extra_args=pandoc_args
            )
            file = default_storage.open(converted_filename, 'rb')
            response = HttpResponse(File(file), MIME_TYPES[out_format])
            default_storage.delete(filename)
            default_storage.delete(converted_filename)
            return response
        else:
            content = pypandoc.convert_text(content, format=pandoc_in, to=pandoc_out)
            return Response({
                'content': content
            })

        
