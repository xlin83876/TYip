import os
import requests  # 确保导入 requests 模块
from github import Github

# 获取 GitHub Token（使用自定义 secret）
GITHUB_TOKEN = os.getenv("MY_GITHUB_TOKEN")
if not GITHUB_TOKEN:
    print("Error: MY_GITHUB_TOKEN is not set.")
    exit(1)

# 从环境变量获取，未设置则直接报错
REPO_NAME = os.getenv("REPO_NAME")
FILE_PATH = os.getenv("FILE_PATH")
WEBPAGE_URL = os.getenv("WEBPAGE_URL")

# 调试输出
print(f"DEBUG: REPO_NAME={REPO_NAME}")
print(f"DEBUG: FILE_PATH={FILE_PATH}")
print(f"DEBUG: WEBPAGE_URL={WEBPAGE_URL}")

if not REPO_NAME or not FILE_PATH or not WEBPAGE_URL:
    print("Error: One or more required environment variables (REPO_NAME, FILE_PATH, WEBPAGE_URL) are not set.")
    exit(1)

def fetch_webpage_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        if not response.text:
            print(f"Warning: Empty content from {url}")
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching CSV: {e}")
        return None

def write_to_github(content):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    try:
        file = repo.get_contents(FILE_PATH)
        repo.update_file(FILE_PATH, "Updated CSV content", content, file.sha, branch="main")
        print("File updated successfully on GitHub.")
    except Exception as e:
        print(f"Error writing to GitHub: {e}")

def main():
    print("Fetching CSV content...")
    content = fetch_webpage_content(WEBPAGE_URL)
    if content:
        print("Writing content to GitHub...")
        write_to_github(content)

if __name__ == "__main__":
    main()
