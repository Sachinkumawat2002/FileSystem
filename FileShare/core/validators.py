# api/validators.py

from django.core.exceptions import ValidationError
import mimetypes

ALLOWED_FILE_TYPES = [
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # .docx
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',        # .xlsx
    'application/vnd.openxmlformats-officedocument.presentationml.presentation' # .pptx
]

def validate_file_type(file):
    mime_type, encoding = mimetypes.guess_type(file.name)
    if mime_type not in ALLOWED_FILE_TYPES:
        raise ValidationError(f'Unsupported file type: {mime_type}. Allowed types are: docx, xlsx, pptx.')
