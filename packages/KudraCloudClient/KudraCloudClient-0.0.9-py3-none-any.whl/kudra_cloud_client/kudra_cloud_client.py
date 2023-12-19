import os
import json
import logging
import mimetypes
import requests
import concurrent.futures
from tusclient import client
from time import sleep

logging = logging.getLogger(__name__)

class KudraCloudClient:
    def __init__(self, token: str):
        """
        Initialize KudraCloud instance.

        Parameters:
        - token (str): Token for authentication.
        """
        assert token, f"Token is required."
        self.token = token
        self.MAX_WORKERS: int = 10
        self.CHUNK_SIZE: int = 25 * 1024 * 1024  # 25MB
        self.API_URL: str = "https://app.builder.ubiai.tools:8000/api/v1/"
        self.UPLOAD_URL: str = "https://app.builder.ubiai.tools/files/"
        self.SINGLE_FILE_UPLOAD_SIZE: int = 25 * 1024 * 1024  # 25MB
        self.TOTAL_UPLOAD_SIZE: int = 500 * 1024 * 1024  # 500MB

    def upload_file(self, filename: str, index: int, total: int, files_dir: str) -> dict:
        """
        Upload a file using tus protocol.

        Parameters:
        - filename (str): The name of the file to be uploaded.
        - index (int): The index of the file in the list of files to be uploaded.
        - total (int): The total number of files to be uploaded.
        - files_dir (str): Directory containing the files.

        Returns:
        dict: A dictionary containing information about the uploaded file.
        """
        file_path = os.path.join(files_dir, filename)
        assert os.path.getsize(file_path) <= self.SINGLE_FILE_UPLOAD_SIZE, f"File {filename} is larger than 25MB. Please split it into smaller files."
        uploader = client.TusClient(self.UPLOAD_URL).uploader(
            file_path=file_path, chunk_size=self.CHUNK_SIZE, retries=3
        )
        sleep(0.1)
        uploader.upload()

        file_info = {
            "file_type": mimetypes.guess_type(file_path)[0],
            "file_name": uploader.url.split("/")[-1],
            "original_name": os.path.basename(file_path),
        }

        logging.warning(f"Uploading file ({index + 1} / {total})")
        return file_info

    def process_entry(self, entry: dict) -> dict:
        """
        Process an entry by formatting its tokens.

        Parameters:
        - entry (dict): The entry to be processed.

        Returns:
        dict: The processed entry with formatted tokens.
        """
        formatted_tokens = [
            {
                "id": token["id"],
                "start": token["start"],
                "end": token["end"],
                "text": token["text"],
                "selected": token.get("selected", False),
            }
            for token in entry["tokens"]
        ]
        formatted_entry = {
            **entry,
            "tokens": formatted_tokens
        }
        return formatted_entry

    def analyze_documents(self, files_dir: str, project_run_id: str) -> tuple:
        """
        Upload files and annotate them.

        Parameters:
        - files_dir (str): Directory containing the files to be uploaded.
        - project_run_id (str): ID of the project run.

        Returns:
        result (list): A list of the processed documents.
        """
        assert os.path.isdir(files_dir), f"Directory {files_dir} does not exist."
        assert len(os.listdir(files_dir)) > 0, f"Directory {files_dir} is empty."
        assert project_run_id, f"Project run ID is required."
        # verify total files size is less than 500MB
        total_size = 0
        for entry in os.scandir(files_dir):
            if entry.is_file():
                total_size += entry.stat().st_size
        logging.warning(f"Total files size: {total_size}")
        assert total_size <= self.TOTAL_UPLOAD_SIZE, f"Total files size is larger than 500MB. Please split it into smaller files."
        formatted_result = []
        files_count = len(os.listdir(files_dir))

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
            files_payload = list(executor.map(self.upload_file, os.listdir(files_dir), range(files_count), [files_count] * files_count, [files_dir] * files_count))

        headers = {"Content-Type": "application/json"}
        payload = {"files": files_payload}

        response = requests.post(self.API_URL + project_run_id, headers=headers, data=json.dumps(payload))

        assert response.status_code == 200, f"Failed to upload files."

        for entry in response.json():
            formatted_entry = self.process_entry(entry)
            formatted_result.append(formatted_entry)

        return formatted_result
