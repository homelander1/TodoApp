import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
import main
from fastapi import status


client = TestClient(main.app)

def test_return_heath_check():
    response = client.get('/healthy')
    assert response.status_code==status.HTTP_200_OK
    assert response.json() == {'status':'Healthy'}

