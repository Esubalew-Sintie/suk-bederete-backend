# utils/supabase_storage.py

import os
import requests
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.utils.deconstruct import deconstructible
import mimetypes

@deconstructible
class SupabaseStorage(Storage):
    def __init__(self, supabase_url=None, supabase_key=None, bucket_name=None):
        self.supabase_url = supabase_url or settings.SUPABASE_URL
        self.supabase_key = supabase_key or settings.SUPABASE_KEY
        self.bucket_name = bucket_name or settings.SUPABASE_BUCKET_NAME
        
        if not self.supabase_url or not self.supabase_key or not self.bucket_name:
            raise ValueError("Supabase URL, key, and bucket name must be provided")

        self.headers = {
            'apikey': self.supabase_key,
            'Authorization': f'Bearer {self.supabase_key}',
        }
        self.base_url = f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}"
        
        # Debugging output
        print(f"Supabase URL: {self.supabase_url}")
        print(f"Supabase Key: {self.supabase_key}")
        print(f"Bucket Name: {self.bucket_name}")
        print(f"Base URL: {self.base_url}")

    def _save(self, name, content):
        path = f"{self.base_url}/{name}"
        mime_type, _ = mimetypes.guess_type(name)
        if mime_type is None:
            mime_type = 'application/octet-stream'  # Default if MIME type can't be determined
        
        files = {'file': (name, content.read(), mime_type)}
        response = requests.post(path, headers=self.headers, files=files)
        if response.status_code != 200:
            raise Exception(f"Failed to upload file to Supabase: {response.content}")
        return name

    def _open(self, name, mode='rb'):
        path = f"{self.base_url}/{name}"
        response = requests.get(path, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve file from Supabase: {response.content}")
        return ContentFile(response.content)

    def exists(self, name):
        path = f"{self.base_url}/{name}"
        response = requests.head(path, headers=self.headers)
        return response.status_code == 200

    def url(self, name):
        return f"{self.base_url}/{name}"
