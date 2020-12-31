import json
from pathlib import Path

from potodo.potodo import exec_potodo

REPO_DIR = Path(__file__).resolve().parent / "fixtures/repository"

config = {
    "path": REPO_DIR,
    "exclude": [REPO_DIR / "excluded", REPO_DIR / "folder" / "excluded.po"],
    "above": 0,
    "below": 100,
    "only_fuzzy": False,
    "hide_reserved": False,
    "counts": False,
    "offline": True,
    "is_interactive": False,
    "exclude_fuzzy": False,
    "only_reserved": False,
    "exclude_reserved": False,
    "show_reservation_dates": False,
    "no_cache": True,
    "matching_files": False,
}


def test_txt_output(capsys):
    exec_potodo(json_format=False, **config)
    captured = capsys.readouterr()

    assert "file1.po" in captured.out
    assert "file2.po" in captured.out
    assert "# /folder/" in captured.out
    assert "file3.po" in captured.out
    assert "1 fuzzy" in captured.out
    assert "2 fuzzy" not in captured.out
    assert "excluded" not in captured.out
    assert "# /folder/subfolder" in captured.out
    assert "file5.po" in captured.out


def test_output(capsys):
    exec_potodo(json_format=True, **config)
    output = json.loads(capsys.readouterr().out)

    expected = [
        {
            "name": "/",
            "percent_translated": 25.0,
            "files": [
                {
                    "name": "/file1",
                    "path": f"{REPO_DIR}/file1.po",
                    "entries": 3,
                    "fuzzies": 1,
                    "translated": 1,
                    "percent_translated": 33,
                    "reserved_by": None,
                    "reservation_date": None,
                },
                {
                    "name": "/file2",
                    "path": f"{REPO_DIR}/file2.po",
                    "entries": 1,
                    "fuzzies": 0,
                    "translated": 0,
                    "percent_translated": 0,
                    "reserved_by": None,
                    "reservation_date": None,
                },
            ],
        },
        {
            "name": "/folder/",
            "percent_translated": 0.0,
            "files": [
                {
                    "name": "/folder/file3",
                    "path": f"{REPO_DIR}/folder/file3.po",
                    "entries": 1,
                    "fuzzies": 0,
                    "translated": 0,
                    "percent_translated": 0,
                    "reserved_by": None,
                    "reservation_date": None,
                },
            ],
        },
        {
            "name": "/folder/subfolder/",
            "percent_translated": 50.0,
            "files": [
                {
                    "name": "/folder/subfolder/file5",
                    "path": f"{REPO_DIR}/folder/subfolder/file5.po",
                    "entries": 2,
                    "fuzzies": 0,
                    "translated": 1,
                    "percent_translated": 50.0,
                    "reserved_by": None,
                    "reservation_date": None,
                },
            ],
        },
    ]

    assert output == expected
