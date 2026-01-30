import uuid
from pathlib import Path

import pytest
import requests
from conftest import get_asset_filename, trigger_sync_seed_assets


@pytest.mark.parametrize("root", ["input", "output"])
def test_prune_deletes_orphaned_seed_asset_when_file_removed(
    root: str,
    http: requests.Session,
    api_base: str,
    comfy_tmp_base_dir: Path,
):
    """Seed asset (hash=NULL) with no file on disk should be pruned after sync."""
    scope = f"prune-orphan-{uuid.uuid4().hex[:6]}"
    case_dir = comfy_tmp_base_dir / root / "unit-tests" / scope
    case_dir.mkdir(parents=True, exist_ok=True)
    name = f"seed_{uuid.uuid4().hex[:8]}.bin"
    fp = case_dir / name

    fp.write_bytes(b"PRUNE_TEST" * 100)

    trigger_sync_seed_assets(http, api_base)

    r1 = http.get(
        api_base + "/api/assets",
        params={"include_tags": f"unit-tests,{scope}", "name_contains": name},
        timeout=120,
    )
    body1 = r1.json()
    assert r1.status_code == 200
    matches = [a for a in body1.get("assets", []) if a.get("name") == name]
    assert matches, "Seed asset should exist after sync"
    assert matches[0].get("asset_hash") is None, "Should be a seed (no hash)"

    fp.unlink()

    trigger_sync_seed_assets(http, api_base)

    r2 = http.get(
        api_base + "/api/assets",
        params={"include_tags": f"unit-tests,{scope}", "name_contains": name},
        timeout=120,
    )
    body2 = r2.json()
    assert r2.status_code == 200
    matches2 = [a for a in body2.get("assets", []) if a.get("name") == name]
    assert not matches2, "Orphaned seed asset should be pruned"


def test_prune_keeps_seed_asset_with_valid_file(
    http: requests.Session,
    api_base: str,
    comfy_tmp_base_dir: Path,
):
    """Seed asset with file still on disk should NOT be pruned."""
    scope = f"prune-keep-{uuid.uuid4().hex[:6]}"
    case_dir = comfy_tmp_base_dir / "input" / "unit-tests" / scope
    case_dir.mkdir(parents=True, exist_ok=True)
    name = f"keep_{uuid.uuid4().hex[:8]}.bin"
    fp = case_dir / name

    fp.write_bytes(b"KEEP_ME" * 100)

    trigger_sync_seed_assets(http, api_base)

    r1 = http.get(
        api_base + "/api/assets",
        params={"include_tags": f"unit-tests,{scope}", "name_contains": name},
        timeout=120,
    )
    body1 = r1.json()
    assert r1.status_code == 200
    matches = [a for a in body1.get("assets", []) if a.get("name") == name]
    assert matches, "Seed asset should exist"
    asset_id = matches[0]["id"]

    trigger_sync_seed_assets(http, api_base)
    trigger_sync_seed_assets(http, api_base)

    r2 = http.get(f"{api_base}/api/assets/{asset_id}", timeout=120)
    assert r2.status_code == 200, "Seed asset with valid file should survive prune"


def test_prune_keeps_hashed_asset_even_without_file(
    http: requests.Session,
    api_base: str,
    comfy_tmp_base_dir: Path,
    asset_factory,
    make_asset_bytes,
):
    """Hashed asset (hash!=NULL) should NOT be deleted by prune, even if file is missing."""
    scope = f"prune-hashed-{uuid.uuid4().hex[:6]}"
    name = "hashed_asset.bin"
    data = make_asset_bytes(name, 2048)

    a = asset_factory(name, ["input", "unit-tests", scope], {}, data)
    aid = a["id"]
    ahash = a["asset_hash"]
    assert ahash is not None, "Should be a hashed asset"

    p = comfy_tmp_base_dir / "input" / "unit-tests" / scope / get_asset_filename(ahash, ".bin")
    assert p.exists()
    p.unlink()

    trigger_sync_seed_assets(http, api_base)

    r = http.get(f"{api_base}/api/assets/{aid}", timeout=120)
    assert r.status_code == 200, "Hashed asset should NOT be pruned even without file"
    d = r.json()
    assert d.get("asset_hash") == ahash


def test_prune_deletes_seed_asset_info_when_orphaned(
    http: requests.Session,
    api_base: str,
    comfy_tmp_base_dir: Path,
):
    """When seed asset is pruned, its AssetInfo should also be deleted."""
    scope = f"prune-info-{uuid.uuid4().hex[:6]}"
    case_dir = comfy_tmp_base_dir / "output" / "unit-tests" / scope
    case_dir.mkdir(parents=True, exist_ok=True)
    name = f"info_test_{uuid.uuid4().hex[:8]}.txt"
    fp = case_dir / name

    fp.write_bytes(b"INFO_TEST_DATA")

    trigger_sync_seed_assets(http, api_base)

    r1 = http.get(
        api_base + "/api/assets",
        params={"include_tags": f"unit-tests,{scope}"},
        timeout=120,
    )
    body1 = r1.json()
    assert r1.status_code == 200
    matches = [a for a in body1.get("assets", []) if a.get("name") == name]
    assert len(matches) == 1
    asset_info_id = matches[0]["id"]

    fp.unlink()
    trigger_sync_seed_assets(http, api_base)

    r2 = http.get(f"{api_base}/api/assets/{asset_info_id}", timeout=120)
    assert r2.status_code == 404, "AssetInfo should be deleted when seed asset is pruned"


def test_prune_handles_multiple_roots(
    http: requests.Session,
    api_base: str,
    comfy_tmp_base_dir: Path,
):
    """Prune should work correctly when syncing multiple roots."""
    scope = f"prune-multi-{uuid.uuid4().hex[:6]}"

    input_dir = comfy_tmp_base_dir / "input" / "unit-tests" / scope
    output_dir = comfy_tmp_base_dir / "output" / "unit-tests" / scope
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_file = input_dir / f"input_{uuid.uuid4().hex[:8]}.bin"
    output_file = output_dir / f"output_{uuid.uuid4().hex[:8]}.bin"
    input_file.write_bytes(b"INPUT_DATA")
    output_file.write_bytes(b"OUTPUT_DATA")

    trigger_sync_seed_assets(http, api_base)

    r1 = http.get(
        api_base + "/api/assets",
        params={"include_tags": f"unit-tests,{scope}"},
        timeout=120,
    )
    body1 = r1.json()
    assert len(body1.get("assets", [])) == 2

    input_file.unlink()

    trigger_sync_seed_assets(http, api_base)

    r2 = http.get(
        api_base + "/api/assets",
        params={"include_tags": f"unit-tests,{scope}"},
        timeout=120,
    )
    body2 = r2.json()
    assets = body2.get("assets", [])
    assert len(assets) == 1, "Only the output asset should remain"
    assert assets[0]["name"] == output_file.name


def test_prune_handles_special_characters_in_path(
    http: requests.Session,
    api_base: str,
    comfy_tmp_base_dir: Path,
):
    """Paths with special SQL LIKE characters (%, _) should be handled correctly."""
    scope = f"prune-special-{uuid.uuid4().hex[:6]}"
    special_dir = comfy_tmp_base_dir / "input" / "unit-tests" / scope / "test_100%_done"
    special_dir.mkdir(parents=True, exist_ok=True)

    name = f"special_{uuid.uuid4().hex[:8]}.bin"
    fp = special_dir / name
    fp.write_bytes(b"SPECIAL_CHAR_TEST")

    trigger_sync_seed_assets(http, api_base)

    r1 = http.get(
        api_base + "/api/assets",
        params={"include_tags": f"unit-tests,{scope}", "name_contains": name},
        timeout=120,
    )
    body1 = r1.json()
    assert r1.status_code == 200
    matches = [a for a in body1.get("assets", []) if a.get("name") == name]
    assert matches, "Asset with special chars in path should be created"

    trigger_sync_seed_assets(http, api_base)

    r2 = http.get(
        api_base + "/api/assets",
        params={"include_tags": f"unit-tests,{scope}", "name_contains": name},
        timeout=120,
    )
    body2 = r2.json()
    matches2 = [a for a in body2.get("assets", []) if a.get("name") == name]
    assert matches2, "Asset with special chars should NOT be falsely pruned"


def test_prune_with_underscore_in_path(
    http: requests.Session,
    api_base: str,
    comfy_tmp_base_dir: Path,
):
    """Underscore in path should be escaped properly in LIKE query."""
    scope = f"prune-underscore-{uuid.uuid4().hex[:6]}"
    underscore_dir = comfy_tmp_base_dir / "input" / "unit-tests" / scope / "my_folder_name"
    underscore_dir.mkdir(parents=True, exist_ok=True)

    name = f"underscore_{uuid.uuid4().hex[:8]}.bin"
    fp = underscore_dir / name
    fp.write_bytes(b"UNDERSCORE_TEST")

    trigger_sync_seed_assets(http, api_base)

    r1 = http.get(
        api_base + "/api/assets",
        params={"include_tags": f"unit-tests,{scope}"},
        timeout=120,
    )
    body1 = r1.json()
    matches = [a for a in body1.get("assets", []) if a.get("name") == name]
    assert matches, "Asset should exist"

    trigger_sync_seed_assets(http, api_base)
    trigger_sync_seed_assets(http, api_base)

    r2 = http.get(
        api_base + "/api/assets",
        params={"include_tags": f"unit-tests,{scope}"},
        timeout=120,
    )
    body2 = r2.json()
    matches2 = [a for a in body2.get("assets", []) if a.get("name") == name]
    assert matches2, "Asset with underscore in path should survive multiple prunes"
