import os
from ..TemplateRunner import TemplateRunner

class DevOpsRunner(TemplateRunner):
    def __init__(self, args, config):
        super().__init__(args, config)
        print(f"""Command:
{args.command}

DevOps Parameters:
GithubPAT={os.environ['GITHUB_PAT']}
DockerhubUser={os.environ['DOCKERHUB_USER']}
DockerhubPasswd={os.environ['DOCKERHUB_PASSWD']}
""")
        if not os.environ['GITHUB_PAT'] or not os.environ['DOCKERHUB_USER'] or not os.environ['DOCKERHUB_PASSWD']:
            raise Exception("check environment variables")

    def setup(self):
        self.run_cmd("sam build")
        self.run_cmd(f"sam deploy --stack-name {self.stack} --parameter-overrides GithubPAT={os.environ['GITHUB_PAT']} DockerhubUser={os.environ['DOCKERHUB_USER']} DockerhubPasswd={os.environ['DOCKERHUB_PASSWD']}")

    def teardown(self):
        self.empty_versioned_s3_bucket(f"artifact-bucket-{self.stack}")
        self.empty_s3_bucket(f"cache-bucket-{self.stack}")
        self.run_cmd("sam delete --no-prompts")
