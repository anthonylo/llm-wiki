from pathlib import Path
import pytest


FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES_DIR


@pytest.fixture
def sample_csv(fixtures_dir) -> Path:
    return fixtures_dir / "sample.csv"


@pytest.fixture
def sample_tsv(fixtures_dir) -> Path:
    return fixtures_dir / "sample.tsv"


@pytest.fixture
def sample_json(fixtures_dir) -> Path:
    return fixtures_dir / "sample.json"


@pytest.fixture
def sample_xlsx(fixtures_dir) -> Path:
    xlsx_path = fixtures_dir / "sample.xlsx"
    if not xlsx_path.exists():
        import subprocess, sys
        subprocess.run([sys.executable, str(Path(__file__).parent / "create_fixtures.py")], check=True)
    return xlsx_path
