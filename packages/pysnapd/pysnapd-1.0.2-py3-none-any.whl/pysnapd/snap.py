#  Copyright (c) Kuba Szczodrzyński 2022-8-24.

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Snap:
    snap_id: str
    name: str
    summary: str = None

    version: str = None
    revision: int = 1
    updated_at: int = 0
    revision_pin: int = 0

    latest_version: str = None
    latest_revision: int = 0
    latest_updated_at: int = 0

    _workdir: Path = None

    def set_workdir(self, workdir: Path) -> None:
        self._workdir = workdir

    @property
    def is_fetched(self) -> bool:
        return all([self.snap_id, self.name])

    @property
    def is_ok(self) -> bool:
        return all([self.is_fetched, self.latest_version, self.latest_revision])

    @property
    def is_installed(self) -> bool:
        return all([self.is_ok, self.version, self.revision, self.snap_path.is_file()])

    @property
    def is_outdated(self) -> bool:
        if self.revision_pin:
            return self.is_installed and self.revision != self.update_revision
        return self.is_installed and self.revision < self.update_revision

    @property
    def update_revision(self) -> int:
        return self.revision_pin or self.latest_revision

    @property
    def update_version(self) -> str:
        return "[PINNED]" if self.revision_pin else self.latest_version

    @property
    def download_url(self) -> str:
        return f"https://api.snapcraft.io/api/v1/snaps/download/{self.snap_id}_{self.update_revision}.snap"

    @property
    def download_path(self) -> Path:
        return self._workdir / "snaps" / f"{self.name}_{self.update_revision}.snap"

    @property
    def snap_path(self) -> Path:
        return self._workdir / "snaps" / f"{self.name}_{self.revision}.snap"

    @property
    def mount_path(self) -> Path:
        return self._workdir / "mnt" / f"{self.name}"

    @property
    def refresh_context(self) -> dict:
        return {
            "instance-key": self.snap_id,
            "snap-id": self.snap_id,
            "tracking-channel": "stable",
            "revision": self.revision,
        }
