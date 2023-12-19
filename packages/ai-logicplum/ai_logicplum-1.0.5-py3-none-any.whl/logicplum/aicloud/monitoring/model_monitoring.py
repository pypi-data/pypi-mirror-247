import requests
from ..config import base_url, api_token


def read_file(file_path):
    with open(file_path, "rb") as file:
        uploaded_filename = file_path.split('\\')[-1]
        content = file.read()
        return uploaded_filename, content
import base64

def aipilot_model_monitoring(client_token,deployment_id,res_type,file_path):
    data = {
        'res_type':res_type,
        'deployment_id': deployment_id
    }
    url = f"{base_url}/training/aipilot/monitor-model"
    # Get The Monitor Graph Of The Deployed Model
    headers = {"Authorization":client_token}
    uploaded_filename, content = read_file(file_path)
    files = {'file': (uploaded_filename, content)}
    # Send the POST request
    response = requests.post(url, data=data, headers=headers,files=files)
    if data.get('res_type') == 'image':
        return response.content
    return response.json()


def comprehensive_model_monitoring(client_token,deployment_id,res_type,file_path):
    data = {
    'res_type':res_type,
    'deployment_id': deployment_id
    }
    url = f"{base_url}/training/comprehensive/monitor-model"
    # Get The Monitor Graph Of The Deployed Model
    headers = {"Authorization":client_token}
    uploaded_filename, content = read_file(file_path)
    files = {'file': (uploaded_filename, content)}
    # Send the POST request
    response = requests.post(url, data=data, headers=headers,files=files)
    if data.get('res_type') == 'image':
        return response.content
    return response.json()