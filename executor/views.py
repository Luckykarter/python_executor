import os
import shutil
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

BASE_DIR = 'executors'
DOCKERFILE = os.path.join(BASE_DIR, 'Dockerfile')

def _execute(folder, python_file):
    pass


@api_view(['POST'])
def execute(request):
    code = request.data
    username = request.query_params.get('username')
    if not username:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    folder_name = os.path.join(BASE_DIR, f'user_{username}')
    if not os.path.isdir(folder_name):
        try:
            os.mkdir(folder_name)
            shutil.copyfile(DOCKERFILE, os.path.join(folder_name, 'Dockerfile'))
        except Exception as e:
            return Response(f'Failed to create dir {folder_name}', status=status.HTTP_400_BAD_REQUEST)

    with open(os.path.join(folder_name, 'code.py'), 'wb') as f:
        f.write(code)

    build_cmd = f"docker build -t image_{username} {folder_name}"
    os.system(build_cmd)

    return Response()

def test_execute(request):
    pass