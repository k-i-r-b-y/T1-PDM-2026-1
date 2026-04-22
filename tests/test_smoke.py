from pathlib import Path
import unittest

from src.etl.config import build_project_paths
from src.etl.region_dim import infer_region


class SmokeTests(unittest.TestCase):
    """Basic import and configuration checks."""

    def test_build_project_paths_uses_repository_root(self) -> None:
        root = Path(__file__).resolve().parents[1]
        paths = build_project_paths(root)
        self.assertEqual(paths.raw_dir, root / "data" / "raw")
        self.assertEqual(paths.warehouse_dir, root / "data" / "warehouse")

    def test_infer_region_defaults_to_unknown(self) -> None:
        self.assertEqual(
            infer_region("Lorem ipsum", "qxzv qxzv qxzv"),
            "Desconocida",
        )


if __name__ == "__main__":
    unittest.main()
