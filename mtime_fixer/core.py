#!/usr/bin/env python3
import os
import stat
from typing import List


class MtimeFixer:
    def __init__(self, fix_ctimes: bool = False, fix_files: bool = False):
        self.fix_ctimes: bool = False
        self.fix_files: bool = fix_files
        self.librt = None

        if fix_ctimes:
            if self._setup_librt():
                self.fix_ctimes = True

    def _setup_librt(self) -> bool:
        global ctypes, timespec
        import ctypes.util

        librt = ctypes.util.find_library("rt")
        if not librt:
            return False
        try:
            self.librt = ctypes.CDLL(librt)
        except Exception:
            return False

        class timespec(ctypes.Structure):
            _fields_ = [("tv_sec", ctypes.c_long),
                        ("tv_nsec", ctypes.c_long)]

        return True

    @staticmethod
    def _enable_ntp() -> None:
        import subprocess
        popen = subprocess.Popen(["timedatectl", "set-ntp", "true"], stdin=subprocess.DEVNULL,
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        try:
            popen.wait(10)
        except subprocess.TimeoutExpired:
            pass

    def _set_time(self, time_ns: int) -> None:
        ts = timespec(time_ns // 1_000_000_000, time_ns % 1_000_000_000)
        self.librt.clock_settime(0, ctypes.byref(ts))

    def _fix_times(self, path: str, time_ns: int) -> None:
        if self.fix_ctimes:
            self._set_time(time_ns)
        os.utime(path, ns=(time_ns, time_ns), follow_symlinks=False)

    def _is_fix_needed(self, stat_: os.stat_result, time_ns: int) -> bool:
        if not self.fix_files and not stat.S_ISDIR(stat_.st_mode):
            return False
        elif self.fix_ctimes and abs(stat_.st_ctime_ns - time_ns) > 1_000_000_000:
            return True
        elif abs(stat_.st_mtime_ns - time_ns) > 1_000_000_000:
            return True
        else:
            return False

    def _fix_path(self, path: str) -> int:
        current_stat = os.stat(path, follow_symlinks=False)
        max_mtime = 0

        if stat.S_ISDIR(current_stat.st_mode):
            for child in os.listdir(path):
                child_mtime = self._fix_path(os.path.join(path, child))
                if child_mtime > max_mtime:
                    max_mtime = child_mtime

        if max_mtime == 0:
            max_mtime = current_stat.st_mtime_ns

        if self._is_fix_needed(current_stat, max_mtime):
            self._fix_times(path, max_mtime)
        return max_mtime

    @staticmethod
    def _disable_ntp() -> bool:
        import subprocess
        try:
            subprocess.run(["timedatectl", "set-ntp", "false"], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, universal_newlines=True, timeout=10)
        except subprocess.TimeoutExpired as e:
            print(f"Failed to disable ntp:\n{e.output}")
            return False
        else:
            return True

    def fix(self, paths: List[str]) -> bool:
        if self.fix_ctimes:
            success = self._disable_ntp()
            if not success:
                return False
            try:
                for path in paths:
                    self._fix_path(path)
            finally:
                self._enable_ntp()
        else:
            for path in paths:
                self._fix_path(path)

        return True
