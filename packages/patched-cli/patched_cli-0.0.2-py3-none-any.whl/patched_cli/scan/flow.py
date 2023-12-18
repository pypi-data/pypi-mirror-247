from typing import Literal

from patched_cli.client.patched import PatchedClient
from patched_cli.models.common import VulnFile
from patched_cli.scan.vuln_provider import SemgrepVulnProvider

def apply_flow(path: str, flow: Literal["semgrep"] | Literal["sonar"], vuln_file: str | None,
               client: PatchedClient) -> list[VulnFile]:
    if flow == "semgrep":
        vuln_provider = SemgrepVulnProvider(path, vuln_file)

    return vuln_provider.run_provider()
