import json
import os

from app.resources.module_profile_builder import build_module_profile


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESOURCES_DIR = os.path.join(REPO_ROOT, "resources")


def _read_module(module_id: str) -> str:
    path = os.path.join(RESOURCES_DIR, "catalog", "modules", f"{module_id}.md")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _canonical_keys(profile: dict) -> dict:
    return {
        item["canonical"]: item
        for item in profile.get("joinKeys", [])
    }


def test_time_series_profiles_share_canonical_date_key():
    average = build_module_profile("averagePePb", _read_module("averagePePb"))
    exposure = build_module_profile("stockExposureTiming", _read_module("stockExposureTiming"))
    stock_count = build_module_profile("hldStockNumTime", _read_module("hldStockNumTime"))

    for profile in (average, exposure, stock_count):
        assert profile["entity"] == "fund"
        assert profile["shape"] == "time_series"
        assert "date" in _canonical_keys(profile)

    assert "TDATE" in _canonical_keys(average)["date"]["rawFields"]
    assert "TDATE" in _canonical_keys(exposure)["date"]["rawFields"]
    assert "XAXISDATA" in _canonical_keys(stock_count)["date"]["rawFields"]


def test_structural_sample_fields_can_be_join_keys_without_becoming_render_fields():
    profile = build_module_profile("hldStockNumTime", _read_module("hldStockNumTime"))

    assert "TDATE" in profile["structuralOnlyFields"]
    assert all(field["rawField"] != "TDATE" for field in profile["fields"])


def test_shenwan_industry_modules_share_taxonomy_and_industry_key():
    module_ids = ["swInduStockAlloca", "swInduStockAnal", "swInduStockVala"]
    profiles = [build_module_profile(module_id, _read_module(module_id)) for module_id in module_ids]

    for profile in profiles:
        assert profile["entity"] == "fund"
        assert profile["shape"] == "cross_section"
        assert profile["taxonomy"] == "SWSR"
        industry_key = _canonical_keys(profile)["industry"]
        assert "industryCode" in industry_key["rawFields"]
        assert "industryName" in industry_key["rawFields"]


def test_different_industry_families_do_not_share_taxonomy():
    sw = build_module_profile("swInduStockAlloca", _read_module("swInduStockAlloca"))
    hs = build_module_profile("hsInduStockAlloca", _read_module("hsInduStockAlloca"))

    assert sw["taxonomy"] == "SWSR"
    assert hs["taxonomy"] == "HS_CUSTOM"
    assert sw["taxonomy"] != hs["taxonomy"]
