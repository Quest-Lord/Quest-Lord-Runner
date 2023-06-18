import os
import scratchattach
from github import Github, InputGitTreeElement

def download_file_from_github(token, repo_name, file_path, local_file_path):
  g = Github(token)
  repo = g.get_repo(repo_name)
  try:
    file_content = repo.get_contents(file_path)
    file_data = base64.b64decode(file_content.content).decode('utf-8')
    with open(local_file_path, 'w', encoding='utf-8') as local_file:
      local_file.write(file_data)
  except Exception as e:
    print(f"Failed to download file {file_path}: {str(e)}")
  return local_file_path

download_file_from_github(os.getenv('TOKEN'), "Quest-Lord/Quest-Lord", "DATA/comments.list", "comments.list")

with open("comments.list", "r") as comments:
  comment = eval(comments.read())

print(comment)
