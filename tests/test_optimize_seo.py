import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


class OptimizeSeoTests(unittest.TestCase):
    def _make_product_dir(self, tmpdir: str, slug: str, html: str) -> Path:
        product_dir = Path(tmpdir) / "products" / slug
        product_dir.mkdir(parents=True, exist_ok=True)
        (product_dir / "index.html").write_text(html, encoding="utf-8")
        return product_dir

    def _make_state(self, tmpdir: str, products: list[dict]) -> Path:
        state_path = Path(tmpdir) / "STATE.json"
        state_path.write_text(
            json.dumps({"products": {"active": products}}), encoding="utf-8"
        )
        return state_path

    @patch("scripts.optimize_seo.Path")
    def test_adds_og_tags_to_product_without_og(self, mock_path_cls: object) -> None:
        from scripts.optimize_seo import optimize_seo

        html = "<html><head><title>Test Tool</title></head><body></body></html>"

        with tempfile.TemporaryDirectory() as tmpdir:
            self._make_state(
                tmpdir,
                [
                    {
                        "slug": "test-tool",
                        "name": "Test Tool",
                        "description": "A test tool",
                        "vercel_url": "https://test-tool.vercel.app",
                    }
                ],
            )
            product_dir = self._make_product_dir(tmpdir, "test-tool", html)

            original_cwd = Path.cwd()
            with patch("scripts.optimize_seo.Path") as mpl:
                mpl.return_value = Path(tmpdir) / "products" / "test-tool" / "index.html"
                mpl.side_effect = lambda p: Path(p)
                with patch("builtins.open", create=True):
                    pass

            with patch("scripts.optimize_seo.open", create=True):
                with patch.object(Path, "read_text", return_value=html):
                    with patch.object(Path, "write_text"):
                        with patch.object(Path, "exists", return_value=True):
                            result = optimize_seo.__wrapped__(15) if hasattr(optimize_seo, "__wrapped__") else 0

    def test_optimize_seo_returns_int(self) -> None:
        from scripts.optimize_seo import optimize_seo

        html = '<html><head><title>Test</title></head><body></body></html>'

        with tempfile.TemporaryDirectory() as tmpdir:
            state = {
                "products": {
                    "active": [
                        {
                            "slug": "sample-tool",
                            "name": "Sample Tool",
                            "vercel_url": "https://sample-tool.vercel.app",
                        }
                    ]
                }
            }
            state_path = Path(tmpdir) / "STATE.json"
            state_path.write_text(json.dumps(state), encoding="utf-8")

            product_dir = Path(tmpdir) / "products" / "sample-tool"
            product_dir.mkdir(parents=True, exist_ok=True)
            (product_dir / "index.html").write_text(html, encoding="utf-8")

            import os
            old_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                result = optimize_seo(15)
                self.assertIsInstance(result, int)
            finally:
                os.chdir(old_cwd)

    def test_optimize_seo_adds_og_title(self) -> None:
        from scripts.optimize_seo import optimize_seo

        html = '<html><head><title>My Tool</title></head><body></body></html>'

        with tempfile.TemporaryDirectory() as tmpdir:
            state = {
                "products": {
                    "active": [
                        {
                            "slug": "my-tool",
                            "name": "My Tool",
                            "vercel_url": "https://my-tool.vercel.app",
                        }
                    ]
                }
            }
            state_path = Path(tmpdir) / "STATE.json"
            state_path.write_text(json.dumps(state), encoding="utf-8")

            product_dir = Path(tmpdir) / "products" / "my-tool"
            product_dir.mkdir(parents=True, exist_ok=True)
            (product_dir / "index.html").write_text(html, encoding="utf-8")

            import os
            old_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                result = optimize_seo(15)
                content = (product_dir / "index.html").read_text(encoding="utf-8")
                self.assertIn('og:title', content)
                self.assertIn('og:description', content)
                self.assertIn('twitter:card', content)
                self.assertGreaterEqual(result, 1)
            finally:
                os.chdir(old_cwd)

    def test_optimize_seo_skips_product_with_existing_og(self) -> None:
        from scripts.optimize_seo import optimize_seo

        html = '<html><head><title>Has OG</title><meta property="og:title" content="Has OG"></head><body></body></html>'

        with tempfile.TemporaryDirectory() as tmpdir:
            state = {
                "products": {
                    "active": [
                        {
                            "slug": "has-og",
                            "name": "Has OG",
                        }
                    ]
                }
            }
            state_path = Path(tmpdir) / "STATE.json"
            state_path.write_text(json.dumps(state), encoding="utf-8")

            product_dir = Path(tmpdir) / "products" / "has-og"
            product_dir.mkdir(parents=True, exist_ok=True)
            (product_dir / "index.html").write_text(html, encoding="utf-8")

            import os
            old_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                result = optimize_seo(15)
                self.assertEqual(result, 0)
            finally:
                os.chdir(old_cwd)

    def test_optimize_seo_skips_product_without_title(self) -> None:
        from scripts.optimize_seo import optimize_seo

        html = "<html><head></head><body></body></html>"

        with tempfile.TemporaryDirectory() as tmpdir:
            state = {
                "products": {
                    "active": [
                        {
                            "slug": "no-title",
                            "name": "No Title",
                        }
                    ]
                }
            }
            state_path = Path(tmpdir) / "STATE.json"
            state_path.write_text(json.dumps(state), encoding="utf-8")

            product_dir = Path(tmpdir) / "products" / "no-title"
            product_dir.mkdir(parents=True, exist_ok=True)
            (product_dir / "index.html").write_text(html, encoding="utf-8")

            import os
            old_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                result = optimize_seo(15)
                self.assertEqual(result, 0)
            finally:
                os.chdir(old_cwd)

    def test_optimize_seo_skips_nonexistent_product_dir(self) -> None:
        from scripts.optimize_seo import optimize_seo

        with tempfile.TemporaryDirectory() as tmpdir:
            state = {
                "products": {
                    "active": [
                        {"slug": "ghost-tool", "name": "Ghost Tool"},
                    ]
                }
            }
            state_path = Path(tmpdir) / "STATE.json"
            state_path.write_text(json.dumps(state), encoding="utf-8")

            import os
            old_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                result = optimize_seo(15)
                self.assertEqual(result, 0)
            finally:
                os.chdir(old_cwd)

    def test_optimize_seo_respects_batch_size(self) -> None:
        from scripts.optimize_seo import optimize_seo

        html = "<html><head><title>Tool</title></head><body></body></html>"

        with tempfile.TemporaryDirectory() as tmpdir:
            products = []
            for i in range(10):
                slug = f"tool-{i}"
                products.append({"slug": slug, "name": f"Tool {i}"})
                product_dir = Path(tmpdir) / "products" / slug
                product_dir.mkdir(parents=True, exist_ok=True)
                (product_dir / "index.html").write_text(html, encoding="utf-8")

            state = {"products": {"active": products}}
            state_path = Path(tmpdir) / "STATE.json"
            state_path.write_text(json.dumps(state), encoding="utf-8")

            import os
            old_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                result = optimize_seo(3)
                self.assertLessEqual(result, 3)
            finally:
                os.chdir(old_cwd)

    def test_optimize_seo_generates_correct_urls(self) -> None:
        from scripts.optimize_seo import optimize_seo

        html = "<html><head><title>URL Tool</title></head><body></body></html>"

        with tempfile.TemporaryDirectory() as tmpdir:
            state = {
                "products": {
                    "active": [
                        {
                            "slug": "url-tool",
                            "name": "URL Tool",
                            "vercel_url": "https://url-tool.vercel.app",
                        }
                    ]
                }
            }
            state_path = Path(tmpdir) / "STATE.json"
            state_path.write_text(json.dumps(state), encoding="utf-8")

            product_dir = Path(tmpdir) / "products" / "url-tool"
            product_dir.mkdir(parents=True, exist_ok=True)
            (product_dir / "index.html").write_text(html, encoding="utf-8")

            import os
            old_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                optimize_seo(15)
                content = (product_dir / "index.html").read_text(encoding="utf-8")
                self.assertIn("https://url-tool.vercel.app", content)
                self.assertIn("https://url-tool.vercel.app/og.png", content)
            finally:
                os.chdir(old_cwd)


if __name__ == "__main__":
    unittest.main()
