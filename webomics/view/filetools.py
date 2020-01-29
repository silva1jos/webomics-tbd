import os


def handle_uploaded_file(f, title):
    file_path = os.path.join(os.path.dirname(__file__), 'files/' + title)
    print(file_path)
    with open(file_path, 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
