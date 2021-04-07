import os
from datetime import date
from django.core.exceptions import ValidationError

def path_and_rename(instance, filename):
    path = "documentos/arquivos/"
    ext = filename.split('.')[-1]
    original = filename.split('.')[0]
    today = date.today()
    data = today.strftime("%d%m%Y")
    filename = '{}+{}.{}'.format(original, data, ext)
    return os.path.join(path, filename)

def validate_file_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Arquivo deve ser PDF')

def validate_file_size(value):
    file_size = value.file.size
    if file_size > 2097152: #2mb
        raise ValidationError('Tamanho máximo de 2mb')
