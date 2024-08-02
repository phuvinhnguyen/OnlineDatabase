import json
from github import Github
from huggingface_hub import HfApi
import os

class AbstractItem(dict):
    def __init__(self, **kwargs):
        super(AbstractItem, self).__init__(**kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_json(self):
        """Serialize the EvaluationAttempt object to a JSON string."""
        return json.dumps(self, indent=4)
    
    def push_to_github(self, token, repo_name, target_path, commit_message=None):
        """
        Pushes the JSON representation of the EvaluationAttempt to a GitHub repository.

        Args:
            token (str): GitHub Personal Access Token.
            repo_name (str): Repository name in the format 'username/repository'.
            target_path (str): The full path in the repository where the file will be saved (e.g., 'folder/filename.json').
            commit_message (str): Commit message for the change.

        Returns:
            str: A message indicating success or failure.
        """
        try:
            if commit_message is None:
                commit_message = f"Update {target_path}"

            # Initialize the GitHub object using the token
            g = Github(token)
            
            # Get the repository object
            repo = g.get_repo(repo_name)
            
            # Serialize the dictionary to a JSON string
            json_content = self.to_json()
            
            # Check if the file already exists in the target path
            try:
                contents = repo.get_contents(target_path)
                # If the file exists, update it
                repo.update_file(contents.path, commit_message, json_content, contents.sha)
                return f"Updated {target_path} in {repo_name}"
            except:
                # If the file does not exist, create it
                repo.create_file(target_path, commit_message, json_content)
                return f"Created {target_path} in {repo_name}"
        except Exception as e:
            return f"An error occurred: {str(e)}"
        
    def push_to_huggingface(self, hf_token, repo_id, path_in_repo, commit_message=None):
        """
        Pushes the JSON representation of the EvaluationAttempt to a Hugging Face repository.

        Args:
            hf_token (str): Hugging Face API token.
            repo_id (str): The ID of the Hugging Face repository (e.g., 'username/repository').
            path_in_repo (str): The path in the Hugging Face repository where the file will be saved.
            commit_message (str): Commit message for the change.

        Returns:
            str: A message indicating success or failure.
        """
        try:
            if commit_message is None:
                commit_message = f"Update {path_in_repo}"
            # Initialize the Hugging Face API
            api = HfApi()
            
            # Serialize the dictionary to a JSON string
            json_content = self.to_json()
            
            # Upload the file to the Hugging Face repository
            api.upload_file(
                path_or_fileobj=json_content.encode('utf-8'),
                path_in_repo=path_in_repo,
                repo_id=repo_id,
                token=hf_token,
                commit_message=commit_message
            )
            return f"Successfully uploaded to {repo_id}/{path_in_repo} on Hugging Face."
        except Exception as e:
            return f"An error occurred: {str(e)}"
    
    def save_to_local(self, local_path):
        with open(local_path, 'w') as wf:
            wf.write(self.to_json())

class AbstractDatabase:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def get_files_from_github(cls, repo_name, folder_path, token=None):
        """
        Retrieves all files from a specific folder in a GitHub repository.

        Args:
            token (str): GitHub Personal Access Token.
            repo_name (str): Repository name in the format 'username/repository'.
            folder_path (str): The path to the folder in the repository (e.g., 'folder/').
        
        Returns:
            dict: A dictionary with filenames as keys and file contents as values.
        """
        try:
            # Initialize the GitHub object using the token
            g = Github(token)
            
            # Get the repository object
            repo = g.get_repo(repo_name)
            
            # Get the contents of the specified folder
            contents = repo.get_contents(folder_path)
            
            # Dictionary to store file content
            file_dict = {}

            # Iterate through the contents
            for content_file in contents:
                # Ensure we are only processing files
                if content_file.type == "file":
                    # Retrieve the content of the file
                    file_content = repo.get_contents(content_file.path).decoded_content.decode()
                    # Store it in the dictionary
                    file_dict[content_file.name] = file_content

            return file_dict
        except Exception as e:
            return f"An error occurred: {str(e)}"

    @classmethod
    def get_files_from_huggingface(cls, repo_id, folder_path, token=None):
        """
        Retrieves all files from a specific folder in a Hugging Face repository.

        Args:
            repo_id (str): Repository ID in the format 'username/repository'.
            folder_path (str): The path to the folder in the repository (e.g., 'folder/').
            token (str, optional): Hugging Face API token for private repos.

        Returns:
            dict: A dictionary with filenames as keys and file contents as values.
        """
        try:
            # Initialize the Hugging Face API object
            api = HfApi(token=token)
            
            # Retrieve the list of files in the folder
            files = api.list_repo_files(repo_id=repo_id, revision='main')  # Adjust revision if needed
            
            # Dictionary to store file content
            file_dict = {}

            # Iterate through the files
            for file_info in files:
                if file_info['path'].startswith(folder_path) and file_info['type'] == 'file':
                    # Retrieve the content of the file
                    file_content = api.download_file(repo_id=repo_id, path=file_info['path'], revision='main')  # Adjust revision if needed
                    # Store it in the dictionary
                    file_dict[file_info['path']] = file_content

            return file_dict
        except Exception as e:
            return f"An error occurred: {str(e)}"
        
    @classmethod
    def get_files_from_local(cls, folder_path):
        """
        Retrieves all files from a specific folder and returns a dictionary
        with filenames as keys and file contents as values.

        Args:
            folder_path (str): Path to the folder containing the files.

        Returns:
            dict: A dictionary with 'filename' as keys and 'file_content' as values.
        """
        file_dict = {}

        # Walk through the folder
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                # Full file path
                file_path = os.path.join(root, file_name)
                
                # Read the file content
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Store the content in the dictionary with the filename as key
                file_dict[file_name] = content

        return file_dict

    @classmethod
    def from_github(cls, repo_name, folder_path, token=None):
        data = cls.get_files_from_github(token, repo_name, folder_path)
        return cls.reduce(data)
    
    @classmethod
    def from_huggingface(cls, repo_id, folder_path, token=None):
        data = cls.get_files_from_huggingface(repo_id, folder_path, token)
        return cls.reduce(data)
    
    @classmethod
    def from_local(cls, folder_path):
        data = cls.get_files_from_local(folder_path)
        return cls.reduce(data)