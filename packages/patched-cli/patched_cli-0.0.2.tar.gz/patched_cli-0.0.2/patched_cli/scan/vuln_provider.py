import json
import os
import pathlib
import subprocess
from collections import defaultdict
from typing import Protocol, Any

from patched_cli.client.sonar import SonarClient
from patched_cli.models.common import VulnFile, Vuln


class VulnProviderProtocol(Protocol):
    def run_provider(self) -> list[VulnFile]:
        ...

    def run_tool(self) -> Any:
        ...

    def read_vuln_file(self) -> Any:
        ...

    def to_vulns(self, raw: Any) -> list[VulnFile]:
        ...


class SemgrepVulnProvider:
    def __init__(self, path: str | pathlib.Path, vuln_file: str | pathlib.Path | None = None):
        self._path = path
        self._vuln_file = vuln_file

    def run_provider(self) -> list[VulnFile]:
        raw = self.read_vuln_file()
        if raw is None:
            raw = self.run_tool()

        return self.to_vulns(raw)

    def run_tool(self) -> Any:
        cmd = ["semgrep", "--config", "auto", "--config", "p/python", self._path, "--json"]
        p = subprocess.run(cmd, capture_output=True, text=True)
        return json.loads(p.stdout)

    def read_vuln_file(self) -> Any:
        if self._vuln_file is None:
            return None
        with open(self._vuln_file, "r") as f:
            return json.load(f)

    def to_vulns(self, raw: dict) -> list[VulnFile]:
        semgrep_result = raw["results"]

        path_vuln_metas = defaultdict(list)
        for result in semgrep_result:
            try:
                cwe = result["extra"]["metadata"]["cwe"]
            except KeyError:
                continue

            if isinstance(cwe, list):
                inner = []
                for cwe_element in cwe:
                    vuln_meta = Vuln(cwe=cwe_element,
                                     bug_msg=result["extra"]["message"],
                                     start=result["start"]["line"],
                                     end=result["end"]["line"])
                    inner.append(vuln_meta)
            else:
                vuln_meta = Vuln(cwe=cwe,
                                 bug_msg=result["extra"]["message"],
                                 start=result["start"]["line"],
                                 end=result["end"]["line"])
                inner = [vuln_meta]
            path_vuln_metas[result["path"]].extend(inner)

        vulns = []
        for path, vuln_metas in path_vuln_metas.items():
            with open(path, 'r') as src_file:
                src = src_file.read()
            vuln = VulnFile(path=path, src=src, vulns=vuln_metas)
            vulns.append(vuln)
        return vulns


class SonarVulnProvider:
    def __init__(self, repo_dir: str, repo_slug: str, access_token: str, url: str = SonarClient.DEFAULT_URL):
        self._repo_dir = repo_dir
        self._project_key = repo_slug.replace("/", "_")
        self._client = SonarClient(access_token, url)

    def run_provider(self) -> Any:
        raw = self.run_tool()
        return self.to_vulns(raw)

    def run_tool(self) -> Any:
        path_vulns = self._client.find_vulns(self._project_key)
        return path_vulns

    def read_vuln_file(self) -> Any:
        pass

    def to_vulns(self, raw: dict) -> list[VulnFile]:
        vuln_files = []
        for path, vulns in raw.items():
            with open(os.path.join(self._repo_dir, path), "r") as fp:
                src = fp.read()
            vuln_file = VulnFile(path=path, src=src, vulns=vulns)
            vuln_files.append(vuln_file)
        return vuln_files
