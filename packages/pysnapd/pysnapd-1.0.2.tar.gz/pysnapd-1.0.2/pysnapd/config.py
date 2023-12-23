#  Copyright (c) Kuba Szczodrzyński 2022-8-24.

from dataclasses import dataclass
from pathlib import Path

import yaml

from .snap import Snap

try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader


@dataclass
class Config(yaml.YAMLObject):
    store_id: str = None
    snaps: list[Snap] = None

    @property
    def data_rw_path(self) -> Path:
        # data storage (R/W)
        return self.workdir / "data-rw"

    @property
    def data_ro_path(self) -> Path:
        # extra data for chroot (R/O)
        return self.workdir / "data-ro"

    @property
    def mnt_path(self) -> Path:
        # snap mount points
        return self.workdir / "mnt"

    @property
    def root_path(self) -> Path:
        # chroot filesystem
        return self.workdir / "root"

    @property
    def snaps_path(self) -> Path:
        # snap downloads
        return self.workdir / "snaps"

    @property
    def work_path(self) -> Path:
        # workdir for overlay mount
        return self.workdir / "work"

    def __init__(self, workdir: Path):
        self.workdir = workdir
        self.config_path = workdir / "config.yaml"
        if self.config_path.is_file():
            self.load()

    def validate(self, interactive: bool = False) -> bool:
        updated = False

        if not self.store_id:
            if not interactive:
                raise RuntimeError("Snap store ID missing")
            self.store_id = input("Enter store ID: ").strip()
            updated = True

        if not self.snaps or interactive:
            if not interactive:
                raise RuntimeError("Snap list missing")
            if not self.snaps:
                self.snaps = []
            name = "dummy"
            while name:
                name = input("Enter snap name (empty to stop): ").strip()
                if not name:
                    break
                snap = Snap(snap_id="", name=name)
                snap.set_workdir(self.workdir)
                revision = input("  Enter revision, or empty to use latest: ").strip()
                if revision and revision.isnumeric():
                    snap.revision_pin = int(revision)
                self.snaps.append(snap)
            updated = True

        if updated:
            self.save()
        else:
            if not all(snap.is_fetched for snap in self.snaps):
                raise ValueError("Invalid configuration, edit and try again")
        return updated

    def load(self):
        with self.config_path.open("r") as f:
            data: dict = yaml.load(f, Loader)
        self.store_id = data.get("store_id", None)
        self.snaps = [Snap(**snap) for snap in data.get("snaps", [])]
        for snap in self.snaps:
            snap.set_workdir(self.workdir)

    def save(self):
        data = dict(
            store_id=self.store_id,
            snaps=[dict(snap.__dict__) for snap in self.snaps],
        )
        for snap in data["snaps"]:
            snap.pop("_workdir", None)
        with self.config_path.open("w") as f:
            yaml.dump(data, f, Dumper, sort_keys=False)
