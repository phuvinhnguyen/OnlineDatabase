from github import Github
from huggingface_hub import HfApi, hf_hub_download
import os

class GitHubManager:
    def __init__(self, token):
        self.github = Github(token)

    def push(self, repo_name, file_path, content, commit_message="Update file") -> str:
        try:
            repo = self.github.get_repo(repo_name)
            try:
                file = repo.get_contents(file_path)
                repo.update_file(file.path, commit_message, content, file.sha)
                return f"Updated {file_path} in {repo_name}."
            except:
                repo.create_file(file_path, commit_message, content)
                return f"Created {file_path} in {repo_name}."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def pull(self, repo_name, file_path) -> str:
        try:
            repo = self.github.get_repo(repo_name)
            file = repo.get_contents(file_path)
            return file.decoded_content.decode('utf-8')
        except Exception as e:
            return f"An error occurred: {str(e)}"

class HuggingFaceRepoManager:
    def __init__(self, hf_token):
        self.hf_api = HfApi(token=hf_token)
        self.token = hf_token

    def push(self, repo_id, file_path, content, commit_message="Update file") -> str:
        try:
            self.hf_api.upload_file(
                path_or_fileobj=content.encode('utf-8'),
                path_in_repo=file_path,
                repo_id=repo_id,
                commit_message=commit_message
            )
            return f"Successfully uploaded {file_path} to {repo_id} on Hugging Face."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def pull(self, repo_id, file_path) -> str:
        try:
            file_dir = hf_hub_download(repo_id=repo_id, filename=file_path, token=self.token)

            with open(file_dir, 'r') as f:
                file_content = f.read()
                os.remove(file_dir)
            return file_content
        except Exception as e:
            return f"An error occurred: {str(e)}"