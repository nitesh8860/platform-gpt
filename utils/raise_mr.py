import gitlab

def create_merge_request(gitlab_token, gitlab_url, project_id, branch_name, file_content, file_name, file_path):
    # Authenticate with GitLab
    gl = gitlab.Gitlab(gitlab_url, private_token=gitlab_token)
    gl.auth()

    try:
        # Get the project
        project = gl.projects.get(project_id)

        # Create a new branch
        branch = project.branches.create({'branch': branch_name, 'ref': 'master'})

        # Create a new file in the branch
        project.files.create({
            'file_path': f"{file_path}/{file_name}",
            'branch': branch_name,
            'content': file_content,
            'commit_message': f"Add {file_name} to {file_path}"
        })

        # Raise a merge request
        merge_request_title = f"Merge {branch_name} into master"
        merge_request_description = f"Please review and merge {branch_name}."

        merge_request = project.mergerequests.create({
            'source_branch': branch_name,
            'target_branch': 'master',
            'title': merge_request_title,
            'description': merge_request_description
        })

        return merge_request
    except Exception as e:
        return None, str(e)

# Example usage:
gitlab_token = "YOUR_GITLAB_TOKEN"
gitlab_url = "https://gitlab.example.com"
project_id = 1  # Replace with your project's ID or name
branch_name = "feature/your-new-branch"  # Replace with your desired branch name
file_content = "This is the content of the file."
file_name = "example.txt"
file_path = "path/to/repo/"  # Replace with your desired path in the repository

merge_request, error_message = create_merge_request(gitlab_token, gitlab_url, project_id, branch_name, file_content, file_name, file_path)

if merge_request:
    print(f"Merge request created: {merge_request.web_url}")
else:
    print(f"Failed to create merge request: {error_message}")
