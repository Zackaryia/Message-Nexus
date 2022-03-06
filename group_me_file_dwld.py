import requests
from json import dumps
import requests


# ! GET ACCESS TOKEN VIA GROUP ME WEBSITE ! #
headers = {
		"x-access-token": f"{access_token}",
}

data = f"{{\"file_ids\":[\"{file_id}\"]}}"

response = requests.post(f"https://file.groupme.com/v1/{group_id}/fileData", headers=headers, data=data)
print(response.ok)
print(response.content)
print(response.text)
print(response.json())
print(response.status_code)
if response.json()[0]['file_id'] == file_id:
	print(response.json()[0]['file_data'])
else:
	print(response.json())
	print(file_id)
	ValueError("File id did not equal file id")
data = {
	"access_token": f"{access_token}",
	"omit-content-disposition": "false"
}

response = requests.post(f"https://file.groupme.com/v1/{group_id}/files/{file_id}", data=data)

print(response.ok)
print(response.content)
print(response.text)
print(response.status_code)

