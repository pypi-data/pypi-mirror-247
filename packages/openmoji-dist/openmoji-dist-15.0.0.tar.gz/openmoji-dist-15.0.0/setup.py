from __future__ import annotations

from pathlib import Path
from warnings import filterwarnings

from openmoji_dist import VERSION, _get_openmoji_data_dir, SVG_SOURCE_URL, FONT_SOURCE_URL, LICENSE_TEXT_URL
from setuptools import setup, find_packages

filterwarnings("ignore", "", UserWarning, "setuptools.dist")

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3 :: Only",
    "Typing :: Typed",
]

OPENMOJI_DIR = Path(_get_openmoji_data_dir())

if (Path(__file__).parent / ".git").exists():
    import shutil
    shutil.rmtree(OPENMOJI_DIR, ignore_errors=True)

if not OPENMOJI_DIR.exists() or not tuple(OPENMOJI_DIR.iterdir()):
    from tempfile import TemporaryDirectory
    from urllib.request import urlretrieve
    from zipfile import ZipFile

    SVG_DEST_DIR = OPENMOJI_DIR / "svg"
    SVG_DEST_DIR.mkdir(exist_ok=True, parents=True)
    FONT_DEST_DIR = OPENMOJI_DIR / "font"
    FONT_DEST_DIR.mkdir(exist_ok=True)

    urlretrieve(LICENSE_TEXT_URL, OPENMOJI_DIR / "LICENSE")

    with TemporaryDirectory() as download_dir:
        svg_file = Path(download_dir) / "svg.zip"
        urlretrieve(SVG_SOURCE_URL, svg_file)
        with ZipFile(svg_file) as zip_file:
            zip_file.namelist()
            zip_file.extractall(SVG_DEST_DIR)

    with TemporaryDirectory() as download_dir:
        font_file = Path(download_dir) / "font.zip"
        urlretrieve(FONT_SOURCE_URL, font_file)
        with ZipFile(font_file) as zip_file:
            for member in zip_file.namelist():
                if "colr" not in member:
                    continue
                if not member.endswith((".woff2", ".ttf")):
                    continue
                zip_file.extract(member=member, path=Path(download_dir))
                name = ("colr1" if "colr1" in member else "colr0") + "." + member.split(".")[-1]
                (FONT_DEST_DIR / name).write_bytes((Path(download_dir) / member).read_bytes())

package_data = {
    OPENMOJI_DIR.parent.relative_to(Path(__file__).parent).as_posix().replace("/", "."): [
        file.relative_to(OPENMOJI_DIR.parent).as_posix()
        for file in OPENMOJI_DIR.rglob("*")
        if file.is_file()
    ]
}

setup(
    name="openmoji-dist",
    license="CC-BY-SA-4.0",
    platforms="OS Independent",
    description="Openmoji files",
    long_description=(Path(__file__).parent / "README").read_text("UTF-8"),
    url="https://codeberg.org/Joshix/py-openmoji",
    version=VERSION,
    classifiers=classifiers,
    packages=find_packages(),
    package_data=package_data,
    include_package_data=True,
)
