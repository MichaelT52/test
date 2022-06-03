# Uploader

import os
import time

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.metadata']
folder_id = "1_e2HXHXaEE1nqd_K8jtHW6f6R_o9bu7X"
upload_folder = "C:/Users/micha/Desktop/Guido/upload"

go = True

def main():
	try:
		service = build('drive', 'v3', credentials=creds)
		
		uploaded = []
		pageToken = None
		while True:
			response = service.files().list(q='trashed = false',
											spaces='drive',
											fields='nextPageToken, files(id, name, parents)',
											pageToken=pageToken).execute()
			for file in response.get('files', []):
				if file.get("parents"):
					if folder_id in file.get("parents"):
						uploaded.append(file.get("name"))
						# print("File:", file.get("name"), file.get("id"))
				
			pageToken = response.get('nextPageToken', None)
			if pageToken is None:
				break

		print(uploaded)
		print(os.listdir(upload_folder))

		if go:
			for file in os.listdir(upload_folder):
				if file not in uploaded:
					print("UPLOADING:", file)
					meta_data = {'name': file, 'parents': [folder_id]}
					media = MediaFileUpload((upload_folder + "/" + file), resumable=True)
					file = service.files().create(body=meta_data,
													media_body=media,
													fields='id').execute()


	except HttpError as e:
		print("Error:", e)


if os.path.exists('token.json'):
	creds = Credentials.from_authorized_user_file('token.json', SCOPES)

if creds:
	main()