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

try:
  download_file_from_github(os.getenv('TOKEN'), "Quest-Lord/Quest-Lord", "DATA/comments.list", "comments.list")

  with open("comments.list", "r") as comments:
    comment = eval(comments.read())

  if len(comment) > 0:
    session = scratch3.login(os.getenv('QUESTLORD_USERNAME'), os.getenv('QUESTLORD_PASSWORD'))

    if comment[0][0] == "profile":
      user = session.connect_user(str(comment[0][1]))
      user.post_comment(str(comment[0][2]), parent_id="", commentee_id="")
except Exception as e:
  print(e)
