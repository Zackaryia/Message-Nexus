import requests
from json import dumps
import requests

# ! GET ACCESS TOKEN VIA GROUP ME WEBSITE ! #
headers = {
    'x-access-token': '{access_token}',
}

data = '{"file_ids":["{file_id}"]}'

response = requests.post('https://file.groupme.com/v1/{group_id}/fileData', headers=headers, data=data)
print(response.ok)
print(response.content)
print(response.text)
print(response.status_code)

data = {
  'access_token': '{access_token}',
  'omit-content-disposition': 'false'
}

response = requests.post('https://file.groupme.com/v1/{group_id}/files/{file_id}', data=data)

print(response.ok)
print(response.content)
print(response.text)
print(response.status_code)

