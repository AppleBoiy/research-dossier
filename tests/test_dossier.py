import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("dossier", ROOT / "scripts" / "dossier.py")
ds = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ds)


class DossierTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name)
        for f in ("papers.json", "claims.json", "synthesis.json"):
            shutil.copy(ROOT / "tests" / "fixtures" / f, self.out / f)

    def tearDown(self):
        self.tmp.cleanup()

    def test_build(self):
        ds.main(["build", "--out", str(self.out)])  # returns normally on success
        for f in ("dossier.html", "dossier.md", "dossier.pandoc.md", "references.bib"):
            self.assertTrue((self.out / f).exists(), f)
        md = (self.out / "dossier.md").read_text()
        self.assertIn("are close [1, 2], with one null result [3]", md)  # numbered in reading order
        self.assertIn("[@", (self.out / "dossier.pandoc.md").read_text())
        html = (self.out / "dossier.html").read_text()
        self.assertNotIn("__BODY__", html)
        self.assertIn('id="ref-', html)

    def test_unknown_citation_is_refused(self):
        syn = json.loads((self.out / "synthesis.json").read_text())
        syn["summary"] += " Invented [@nobody2099fake]."
        (self.out / "synthesis.json").write_text(json.dumps(syn))
        with self.assertRaises(SystemExit) as e:
            ds.main(["build", "--out", str(self.out)])
        self.assertIsInstance(e.exception.code, str)  # sys.exit("fix the errors …")
        self.assertFalse((self.out / "dossier.html").exists())


if __name__ == "__main__":
    unittest.main()
