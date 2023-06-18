import os
import scratchattach as scratch3
from github import Github, InputGitTreeElement
import base64

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

def upload_or_replace_file(token, repo_name, local_file_path, github_file_path, commit_message):
  g = Github(token)
  repo = g.get_repo(repo_name)
  with open(local_file_path, 'r') as file:
    content = file.read()
  try:
    contents = repo.get_contents(github_file_path)
    repo.update_file(contents.path, commit_message, content, contents.sha)
  except:
    repo.create_file(github_file_path, commit_message, content)

try:
  download_file_from_github(os.getenv('TOKEN'), "Quest-Lord/Quest-Lord", "DATA/comments.list", "comments.list")
  
  with open("comments.list", "r") as comments:
    comment = eval(comments.read())
  
  if len(comment) > 0:
    comment_post = comment.pop(0)
    with open("comments.list", "w") as comments:
      comments.write(str(comment))
  
    upload_or_replace_file(os.getenv('TOKEN'), "Quest-Lord/Quest-Lord", "comments.list", "DATA/comments.list", "Posted Comment")
  
    session = scratch3.login(os.getenv('QUESTLORD_USERNAME'), os.getenv('QUESTLORD_PASSWORD'))
  
    if comment_post[0] == "profile":
      user = session.connect_user(str(comment_post[1]))
      print(user.post_comment(str(comment_post[2]), parent_id="", commentee_id=""))
except Exception as e:
  print(e)
