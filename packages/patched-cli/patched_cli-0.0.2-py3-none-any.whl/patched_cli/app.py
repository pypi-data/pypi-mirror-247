import pathlib
from typing import Literal

import click
from click_option_group import optgroup, MutuallyExclusiveOptionGroup
import sentry_sdk
from git import Repo, InvalidGitRepositoryError

from patched_cli.client.scm import GithubClient, GithubClientClickType, GitlabClientClickType, ScmPlatformClientProtocol, \
    GitlabClient
from patched_cli.client.patched import PatchedClient, PatchedClientClickType
from patched_cli.git_helpers.git_helpers import create_branch_and_pr
from patched_cli.scan.common import apply_file_changes
from patched_cli.scan.flow import apply_flow

sentry_sdk.init(
    dsn="https://851250f33454ef7fe75cdcdbc6ecaef5@o4506197015330816.ingest.sentry.io/4506221506134016",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


@click.command
@click.version_option(message="%(version)s")
@click.argument("path", type=click.Path(exists=True, file_okay=False, resolve_path=True), default=pathlib.Path.cwd())
@click.option(
    "patched_client", "-t", "--access-token",
    help="Patched Access Token, can be generated through https://app.patched.codes/signin -> Integrations. "
         "This can be set with environment variable \"PATCHED_ACCESS_TOKEN\".",
    envvar="PATCHED_ACCESS_TOKEN", required=True,
    type=PatchedClientClickType(), default=PatchedClientClickType.default, callback=PatchedClientClickType.callback)
@click.option(
    "is_create_pr", "-P", "--create-pr",
    help="Create a pull request. \n"
         "With the current branch as the base branch and the head branch as the patched branch.",
    is_flag=True, default=False, show_default=True)
@click.option(
    "platform_url", "--platform-url",
    help="SCM Platform's URL. "
         f"Default value for Github is \"{GithubClient.DEFAULT_URL}\". "
         f"Default value for Gitlab is \"{GitlabClient.DEFAULT_URL}\". ",
    envvar="PATCHED_SCM_PLATFORM_URL", type=str)
@optgroup("Source Control Management Platform Token", cls=MutuallyExclusiveOptionGroup)
@optgroup.option(
    "github_client", "--github-access-token",
    help="""
        Github's Personal Access Token, can be generated from \"https://github.com/settings/tokens\". 
        This can be set with environment variable \"PATCHED_GITHUB_TOKEN\".
        """,
    envvar="PATCHED_GITHUB_TOKEN", type=GithubClientClickType())
@optgroup.option(
    "gitlab_client", "--gitlab-access-token",
    help="""
        Gitlab's Personal Access Token, can be generated from \"https://gitlab.com/-/profile/personal_access_tokens\".
        This can be set with environment variable \"PATCHED_GITLAB_TOKEN\". 
        """,
    envvar="PATCHED_GITLAB_TOKEN", type=GitlabClientClickType())
@click.option(
    "is_non_git", "--non-git", help="Apply patches to a non-git local directory.",
    is_flag=True, default=False, show_default=True)
@click.option(
    "is_allow_dirty", "--dirty", help="Apply patches to a dirty git repository.",
    is_flag=True, default=False, show_default=True)
@click.option(
    "flow", "--flow", help="Scan flow",
    type=click.Choice(["semgrep"], case_sensitive=False),
    default="semgrep", show_default=True)
@click.option(
    "vuln_report", "--vuln", help="Vulnerability Report based on flow.",
    type=click.Path(exists=True, file_okay=True, resolve_path=True, dir_okay=False))
@click.option(
    "validate", "--validate", help="Validate patch.",
    is_flag=True, default=False, show_default=True)
def main(path: str,
         patched_client: PatchedClient,
         platform_url: str | None,
         github_client: GithubClient | None,
         gitlab_client: GitlabClient | None,
         is_create_pr: bool,
         is_non_git: bool,
         is_allow_dirty: bool,
         flow: Literal["sonar", "semgrep"],
         vuln_report: str | None,
         validate: bool):
    platform_client: ScmPlatformClientProtocol | None = github_client or gitlab_client
    repo = _validations(is_allow_dirty, is_non_git, path, platform_client, platform_url)

    vuln_files = apply_flow(path, flow, vuln_report, patched_client)
    if len(vuln_files) < 1:
        click.echo("No vulnerabilities found.")
        exit(0)
    for vuln_file in vuln_files:
        click.echo(f"Found {len(vuln_file.vulns)} Vulnerabilities at {vuln_file.path}")
    vuln_count = sum(len(vuln_file.vulns) for vuln_file in vuln_files)

    click.echo("Begin generating patches.....")
    try:
        patches = patched_client.get_patches(pathlib.Path(path), repo, vuln_files)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        click.echo(f"Unexpected error: {e}")
        exit(1)

    if len(patches) < 1:
        click.echo(f"No patches generated")
        exit(0)

    click.echo("Applying patches.....")
    changed_files = apply_file_changes(path, patches)
    if len(changed_files) < 1 or (repo is not None and len(repo.git.diff()) < 1):
        click.echo("No files patched!")
        exit(0)
    click.echo("Patched!")

    if validate:
        new_vuln_files = apply_flow(path, flow, vuln_report, patched_client)
        new_vuln_count = sum(len(vuln_file.vulns) for vuln_file in new_vuln_files)
        percent = (1 - new_vuln_count / vuln_count) * 100
        click.echo(f"Fixed {round(percent, 2)}% vulnerabilities")

    if repo is not None:
        result = create_branch_and_pr(path, repo, changed_files, is_create_pr, platform_client, patched_client)
        click.echo(result.message)


def _validations(is_allow_dirty: bool, is_non_git: bool, path: str,
                 platform_client: ScmPlatformClientProtocol | None, platform_url: str | None) -> Repo | None:
    repo = None
    try:
        repo = Repo(path)
    except InvalidGitRepositoryError:
        if not is_non_git:
            click.echo(f"Path: \"{path}\" is not a git repository. "
                       f"To patch a non-git local repository, please use the \"--non-git\" flag.", err=True)
            exit(1)

    if not is_allow_dirty and repo is not None and repo.is_dirty(untracked_files=True):
        click.echo(f"Path: \"{path}\" is a git repository, but it is dirty. "
                   f"To patch a dirty git repository, please use the \"--dirty\" flag.", err=True)
        exit(1)

    # TODO: remove this side effect
    if platform_client is not None and platform_url is not None:
        platform_client.set_url(platform_url)

    if platform_client is not None and not platform_client.test():
        click.echo(f"Unable to access SCM Platform at \"{platform_url}\" with provided token.", err=True)
        exit(1)

    # TODO: remove this return
    return repo


if __name__ == "__main__":
    main()
