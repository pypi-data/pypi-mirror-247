from dataclasses import dataclass


@dataclass(slots=True)
class PrCreationResult:
    message: str
    branch_name: str
    pr_url: str | None