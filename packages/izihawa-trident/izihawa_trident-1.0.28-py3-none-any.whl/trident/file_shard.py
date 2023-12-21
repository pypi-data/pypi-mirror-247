import asyncio
import glob
import logging
import os
import time
import urllib.parse
from dataclasses import dataclass

import aiofiles.os

from .key_cache import KeyCache


@dataclass
class IntegrityReport:
    old_temporary_files: list[str]
    empty_file: list[str]

class FileShard:
    def __init__(self, name: str, path: str):
        self._name = name
        self._path = path
        self._key_cache = KeyCache()
        self._last_integrity_report = None
        asyncio.get_event_loop().run_in_executor(None, self._check_integrity)

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> str:
        return self._path

    async def read(self, key: str) -> bytes:
        file_path = os.path.join(self.path, urllib.parse.quote(key))
        if key in self._key_cache or os.path.exists(file_path):
            self._key_cache.add(key)
            async with aiofiles.open(file_path, "rb") as f:
                return await f.read()

    async def exists(self, key: str) -> bool:
        file_path = os.path.join(self.path, urllib.parse.quote(key))
        if key in self._key_cache or os.path.exists(file_path):
            self._key_cache.add(key)
            return True
        return False

    async def write(self, key: str, value: bytes):
        file_path = os.path.join(self.path, urllib.parse.quote(key))
        tmp_file_path = os.path.join(self.path, '~' + urllib.parse.quote(key))
        async with aiofiles.open(tmp_file_path, "wb") as f:
            await f.write(value)
            await f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_file_path, file_path)
        self._key_cache.add(key)

    def _check_integrity(self) -> IntegrityReport:
        old_temporary_files = []
        empty_file = []
        current_time = time.time()
        for infile in glob.iglob(os.path.join(self._path, '*.*')):
            key = os.path.basename(infile)
            m_time = os.path.getmtime(infile)
            if m_time < current_time - 3600 * 4:
                if key.startswith('~') or key.endswith('~'):
                    old_temporary_files.append(infile)
                    continue
                if os.path.getsize(infile) == 0:
                    empty_file.append(infile)
                    continue
            self._key_cache.add(key)
        self._last_integrity_report = IntegrityReport(
            old_temporary_files=old_temporary_files,
            empty_file=empty_file,
        )
        return self._last_integrity_report

    def get_integrity_report(self) -> IntegrityReport | None:
        return self._last_integrity_report
