import os


def user_directory_path(instance, filename):
    """ Called to save files MEDIA_ROOT/<file_type>/<filename>"""
    return 'user_{0}/{1}'.format(instance.file_type, filename)


def handle_uploaded_file(f, title):
    file_path = os.path.join(os.path.dirname(__file__), 'files/' + title)
    print(file_path)
    with open(file_path, 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
