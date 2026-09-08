import importlib.util
import io
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("vendor", Path(__file__).parents[1] / "scripts/vendor-hugeicons.py")
vendor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vendor)

class ArchiveSecurityTests(unittest.TestCase):
    def archive(self, name, kind=tarfile.REGTYPE):
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w") as archive:
            entry = tarfile.TarInfo(name)
            entry.type = kind
            entry.linkname = "../../outside"
            entry.size = 2 if kind == tarfile.REGTYPE else 0
            archive.addfile(entry, io.BytesIO(b"ok") if entry.size else None)
        buf.seek(0)
        return tarfile.open(fileobj=buf)

    def test_normal_package(self):
        with tempfile.TemporaryDirectory() as dest, self.archive("package/dist/esm/TestIcon.js") as archive:
            vendor.extract_package(archive, dest)
            self.assertEqual((Path(dest)/"package/dist/esm/TestIcon.js").read_text(), "ok")

    def test_rejects_unsafe_members(self):
        cases = [("../outside", tarfile.REGTYPE), ("/tmp/outside", tarfile.REGTYPE),
                 ("package/../../outside", tarfile.REGTYPE), ("other/file", tarfile.REGTYPE),
                 ("package/link", tarfile.SYMTYPE), ("package/link", tarfile.LNKTYPE),
                 ("package/pipe", tarfile.FIFOTYPE)]
        for name, kind in cases:
            with self.subTest(name=name, kind=kind), tempfile.TemporaryDirectory() as dest, self.archive(name, kind) as archive:
                with self.assertRaises(ValueError): vendor.extract_package(archive, dest)
                self.assertEqual(list(Path(dest).iterdir()), [])

    def test_no_unsafe_fallback(self):
        with tempfile.TemporaryDirectory() as dest, self.archive("package/file") as archive:
            with patch.object(vendor.tarfile, "data_filter", create=True):
                del vendor.tarfile.data_filter
                with self.assertRaises(RuntimeError): vendor.extract_package(archive, dest)
            self.assertEqual(list(Path(dest).iterdir()), [])

    def test_rejects_moving_versions_before_download(self):
        with patch.object(vendor.subprocess, "run") as run:
            for version in ["latest", "^4.2.3", "4.2.3 --flag", "https://example.com"]:
                with self.assertRaises(ValueError): vendor.fetch(version, ".")
            run.assert_not_called()

if __name__ == "__main__": unittest.main()
