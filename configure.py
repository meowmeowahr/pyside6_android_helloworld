import os
import zipfile
import logging
import shutil
import PySide6
from jinja2 import Environment, FileSystemLoader
import requests
from pathlib import Path
from tqdm import tqdm

logging.basicConfig(level=logging.DEBUG)

# === Configuration ===

QT_MODULES = ["Core", "Widgets", "Gui"]
QT_VERSION = "6.9.1"

QT_DIR = Path(".qt")
DEPLOYMENT_DIR = Path("deployment")
PYTHON_TAG = "cp311-cp311"
ABI = "android_aarch64"


def download_file(url: str, dest: Path):
    if dest.exists():
        logging.info(f"[SKIP] Already downloaded: {dest}")
        return
    logging.info(f"[DOWNLOAD] {url}")
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        total = int(response.headers.get("content-length", 0))
        with (
            open(dest, "wb") as file,
            tqdm(
                desc=f"Downloading {dest.name}",
                total=total,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
            ) as bar,
        ):
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                bar.update(len(chunk))
    logging.info(f"[DONE] Saved to {dest}")


def extract_and_copy_jar(wheel_path: Path, target_dir: Path) -> Path | None:
    jar_extract_dir = target_dir / "jar"
    jar_extract_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(wheel_path, "r") as archive:
        jar_files = [f for f in archive.namelist() if f.startswith("PySide6/jar/")]
        if not jar_files:
            logging.warning("No .jar files found in wheel.")
            return None

        with tqdm(total=len(jar_files), desc="Extracting .jar files") as bar:
            for f in jar_files:
                archive.extract(f, jar_extract_dir)
                bar.update(1)

    return (jar_extract_dir / "PySide6" / "jar").resolve()


def ensure_templates_exist():
    shutil.copytree(
        Path(os.path.abspath(PySide6.__file__)).parent
        / "scripts"
        / "deploy_lib"
        / "android"
        / "recipes",
        ".tmp/recipes",
        dirs_exist_ok=True,
    )


def create_recipe(
    version: str,
    component: str,
    wheel_path: str,
    generated_files_path: Path,
    qt_modules: list[str],
    local_libs: list[str] | None = None,
    plugins: list[str] | None = None,
):
    """
    Create python_for_android recipe for PySide6 and shiboken6
    """
    qt_plugins = []
    if plugins:
        # split plugins based on category
        for plugin in plugins:
            plugin_category, plugin_name = plugin.split("_", 1)
            qt_plugins.append((plugin_category, plugin_name))

    qt_local_libs = []
    if local_libs:
        qt_local_libs = [
            local_lib for local_lib in local_libs if local_lib.startswith("Qt6")
        ]

    rcp_tmpl_path = Path(".tmp") / "recipes" / f"{component}"
    environment = Environment(loader=FileSystemLoader(rcp_tmpl_path))
    template = environment.get_template("__init__.tmpl.py")
    content = template.render(
        version=version,
        wheel_path=wheel_path,
        qt_modules=qt_modules,
        qt_local_libs=qt_local_libs,
        qt_plugins=qt_plugins,
    )

    recipe_path = generated_files_path / "recipes" / f"{component}"
    recipe_path.mkdir(parents=True, exist_ok=True)
    logging.info(f"[DEPLOY] Writing {component} recipe into {str(recipe_path)}")
    with open(recipe_path / "__init__.py", mode="w", encoding="utf-8") as recipe:
        recipe.write(content)


def main():
    logging.info(f"[INFO] Qt Version: {QT_VERSION}")

    shiboken_whl = f"shiboken6-{QT_VERSION}-{QT_VERSION}-{PYTHON_TAG}-{ABI}.whl"
    pyside_whl = f"PySide6-{QT_VERSION}-{QT_VERSION}-{PYTHON_TAG}-{ABI}.whl"

    shiboken_url = (
        f"https://download.qt.io/official_releases/QtForPython/shiboken6/{shiboken_whl}"
    )
    pyside_url = (
        f"https://download.qt.io/official_releases/QtForPython/pyside6/{pyside_whl}"
    )

    QT_DIR.mkdir(parents=True, exist_ok=True)
    (DEPLOYMENT_DIR / "jar").mkdir(parents=True, exist_ok=True)

    download_file(shiboken_url, QT_DIR / shiboken_whl)
    download_file(pyside_url, QT_DIR / pyside_whl)

    extract_and_copy_jar(QT_DIR / pyside_whl, DEPLOYMENT_DIR)

    ensure_templates_exist()
    create_recipe(
        QT_VERSION, "PySide6", str(QT_DIR / pyside_whl), Path("deployment"), QT_MODULES
    )
    create_recipe(
        QT_VERSION,
        "shiboken6",
        str(QT_DIR / shiboken_whl),
        Path("deployment"),
        QT_MODULES,
    )

    logging.info("[DONE] Deployment setup complete.")
    shutil.rmtree(".tmp")
    logging.info("[DONE] Cleaned up.")


if __name__ == "__main__":
    main()
