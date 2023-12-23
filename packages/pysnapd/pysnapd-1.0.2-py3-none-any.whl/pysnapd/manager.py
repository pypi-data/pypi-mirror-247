#  Copyright (c) Kuba Szczodrzyński 2022-8-24.

from datetime import datetime
from time import time

import requests

from .config import Config
from .snap import Snap
from .utils import command, error, error_exit, info, warn


class SnapManager:
    config: Config

    def __init__(self, config: Config):
        self.config = config

    def headers(self, content_type: str = None):
        headers = {
            "Snap-Device-Architecture": "armhf",
            "Snap-Device-Series": "16",
            "Snap-Device-Store": self.config.store_id,
        }
        if content_type:
            headers["Content-Type"] = content_type
        return headers

    def fetch(self) -> bool:
        if not self.config.snaps:
            return False
        if all(snap.is_fetched for snap in self.config.snaps):
            return False
        info("Fetching snap IDs...")
        url = "https://api.snapcraft.io/v2/snaps/find"
        with requests.get(url, headers=self.headers()) as r:
            data = r.json()
        ids: dict[str, str] = {}
        for result in data["results"]:
            ids[result["name"]] = result["snap-id"]
        for snap in self.config.snaps:
            if snap.name not in ids:
                error("Snap not found:", snap)
            snap.snap_id = ids[snap.name]
        error_exit()
        self.config.save()
        return True

    def refresh(self) -> bool:
        refreshable: list[Snap] = []
        for snap in self.config.snaps:
            if not snap.is_ok or snap.is_installed:
                refreshable.append(snap)
        if not refreshable:
            return False
        info("Refreshing", len(refreshable), "out of", len(self.config.snaps), "snaps")
        url = "https://api.snapcraft.io/v2/snaps/refresh"
        headers = self.headers("application/json")
        data = dict(
            context=[snap.refresh_context for snap in refreshable],
            actions=[dict(action="refresh-all")],
        )
        with requests.post(url, json=data, headers=headers) as r:
            data = r.json()
        not_refreshed = [snap.name for snap in refreshable]
        for result in data["results"]:
            try:
                snap = next(
                    snap for snap in refreshable if snap.snap_id == result["snap-id"]
                )
            except StopIteration:
                warn("Got unknown snap in response:", result)
                continue
            snap.name = result["snap"]["name"]
            snap.summary = result["snap"]["summary"]
            snap.latest_version = result["snap"]["version"]
            snap.latest_revision = result["snap"]["revision"]
            snap.latest_updated_at = int(
                datetime.strptime(
                    result["released-at"][:19],
                    "%Y-%m-%dT%H:%M:%S",
                ).timestamp()
            )
            if snap.name in not_refreshed:
                not_refreshed.remove(snap.name)
        if not_refreshed:
            error("Failed to refresh snaps:", ", ".join(not_refreshed))
            exit(1)
        self.config.save()
        return True

    def install(self, dry_run: bool = False):
        updated = False
        for snap in self.config.snaps:
            if snap.is_installed and not snap.is_outdated:
                info("Snap", snap.name, "up-to-date")
                continue
            if not snap.is_installed:
                info(
                    f"Installing {snap.name} {snap.update_version} (revision {snap.update_revision})"
                )
            elif snap.is_outdated:
                if snap.revision_pin:
                    info(
                        f"Reinstalling {snap.name}: pinned revision {snap.update_revision}"
                    )
                else:
                    info(
                        f"Updating {snap.name}: {snap.version} -> {snap.update_version} ({snap.revision} -> {snap.update_revision})"
                    )
            else:
                error("what?")
                exit(1)

            if dry_run:
                updated = True
                continue

            info("Downloading", snap.download_path)
            updating = snap.is_installed
            size = 0
            with requests.get(snap.download_url, stream=True) as r:
                with snap.download_path.open("wb") as f:
                    for chunk in r.iter_content(128 * 1024):
                        f.write(chunk)
                        size += len(chunk)
            info("Saved", size, "bytes")
            if updating:
                snap.snap_path.unlink(missing_ok=True)
            snap.version = snap.update_version
            snap.revision = snap.update_revision
            snap.updated_at = int(time())
            updated = True
        if updated and not dry_run:
            self.config.save()
        return updated

    def mount_snaps(self):
        for snap in self.config.snaps:
            if not snap.is_installed:
                continue
            info("Mounting snap:", snap.name)
            cmd = "mount -o ro,loop"
            snap.mount_path.mkdir(parents=True, exist_ok=True)
            command(*cmd.split(" "), snap.snap_path, snap.mount_path)

    def mount_root(self, *binds: str):
        info("Mounting overlay chroot filesystem")
        lower_dirs = [self.config.data_ro_path]
        lower_dirs += [snap.mount_path for snap in self.config.snaps]
        upper_dir = self.config.data_rw_path
        work_dir = self.config.work_path
        root = self.config.root_path
        opts = dict(
            rw=None,
            lowerdir=":".join(str(path) for path in lower_dirs),
            upperdir=upper_dir,
            workdir=work_dir,
        )
        opts = ",".join(f"{k}={v}" if v else k for k, v in opts.items())
        cmd = "mount -t overlay -o"
        command(*cmd.split(" "), opts, "overlayfs", root)

        for bind in binds:
            if ":" in bind:
                source, _, target = bind.partition(":")
            else:
                source = target = bind
            if not target.startswith("/"):
                raise ValueError(f"Bind-mount target path must start with / - {target}")
            target = target[1:]
            target_path = root / target
            info(f"Binding {source} at {target_path}")
            target_path.mkdir(parents=True, exist_ok=True)
            cmd = f"mount --bind {source}"
            command(*cmd.split(" "), target_path)

    def unmount_root(self, *binds: str):
        root = self.config.root_path
        for bind in binds:
            if ":" in bind:
                _, _, target = bind.partition(":")
            else:
                target = bind
            if not target.startswith("/"):
                raise ValueError(f"Bind-mount target path must start with / - {target}")
            target = target[1:]
            target_path = root / target
            info(f"Unbinding {target_path}")
            command("umount", "-R", target_path)
        info("Unmounting chroot filesystem")
        command("umount", "-R", root)

    def unmount_snaps(self):
        for snap in self.config.snaps:
            if not snap.is_installed:
                continue
            info("Unmounting snap:", snap.name)
            command("umount", "-R", snap.mount_path)
