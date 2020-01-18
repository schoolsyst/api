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
        return Note.objects.filter(subject__user__id=user.id)

    @action(methods=['get', 'post'], detail=True)
    def convert(self, request, uuid_or_in_format, out_format):
        print(dir(request.data))
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
            note = Note.objects.get(uuid=uuid_or_in_format)
            in_format = note.format.lower()
            content = note.content
            title = note.name
        
        pandoc_in = PANDOC_FORMATS.get(in_format, in_format)
        pandoc_out = PANDOC_FORMATS.get(out_format, out_format)
        
        if pandoc_out in FILE_ONLY_FORMATS:
            filename = f'temp-{uuid.uuid4()}'
            default_storage.save(filename, ContentFile(
                f'<head><title>{title}</title></head><body>{content}</body>'
            ))
            converted_filename = filename+'-converted.'+pandoc_out
            pandoc_args = []
            if pandoc_out == 'pdf':
                css_filepath = default_storage.open('css_resources/pandoc.css').name
                pypandoc.convert_file(
                    default_storage.open(filename).name,
                    format=pandoc_in,
                    outputfile=converted_filename,
                    to="html5",
                    extra_args=(
                        '--standalone',
                        '--pdf-engine', 'wkhtmltopdf',
                        '-c', css_filepath,
                    )
                )
            else:
                pypandoc.convert_file(
                    default_storage.open(filename).name,
                    format=pandoc_in,
                    to=pandoc_out,
                    outputfile=converted_filename,
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
            
    @action(methods=['get'], detail=True)
    def thumbnail(self, request, uuid):
        """ Generate the note's png thumbnail
        
        GET /notes/:uuid/thumbnail
        
        :type uuid: str
        :param uuid: The note's UUID
        """
        import imgkit
        # from thumbnails import get_thumbnail
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        import os
        from backend.settings import BASE_DIR
        from uuid import uuid4
        # Get the note
        note = Note.objects.get(uuid=uuid)
        # If the note is not HTML, we can't generate a thumb.
        if note.format != 'HTML': 
            return None
        # Get the css filename
        css  = default_storage.open('css_resources/pandoc.css').name
        # Add a transparent background
        content = '<body class="transparent">' + note.content + '</body>'
        # Create the output image temp file
        filename = f'temp-{uuid4()}.png'
        filepath = os.path.join(BASE_DIR, filename)
        # Generate the image
        print(f"Generating {filename}")
        try:
            imgkit.from_string(content, filepath, css=css, options={
                'format': 'png',
            })
        except OSError as error:
            #FIXME: Gives errors because it can't load the fonts...
            if os.path.isfile(filepath):
                pass
            else:
                raise error
        print("Generated.")
        # Get the png file
        file = default_storage.open(filename, 'rb')
        # # Thumbnail it
        # get_thumbnail(filepath, '250x350', crop='bottom', scale_up=True, force=True).save(filepath)
        # Prepare the response
        response = HttpResponse(File(file), 'image/png')
        # Delete the temp file
        default_storage.delete(filename)
        # Return the response
        return response
        
        
