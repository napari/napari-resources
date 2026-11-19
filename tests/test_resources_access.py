import importlib.resources as resources

import pytest

from napari_resources import logo_path, logo_templates, logo_variants, special_logo_path, special_logos

# These tests validate the packaging contract: the generated SVGs must be
# present at runtime, either because they were packaged in the wheel or because
# the build hook generated them during an editable install (`uv sync` /
# `pip install -e .`). If you run pytest from a fresh source checkout without
# installing first, they will fail with a helpful error.


def test_logo_resource_reachable_via_importlib():
    path = resources.files("napari_resources.resources.logos") / "generated" / "gradient-plain-dark.svg"
    assert path.is_file()


def test_logo_path_helper():
    assert logo_path().is_file()
    assert logo_path("flat", "text", "light").is_file()


def test_logo_path_missing_raises():
    with pytest.raises(ValueError):
        logo_path("not", "real", "dark")


def test_logo_variants_and_templates():
    variants = logo_variants()
    templates = logo_templates()
    assert "gradient" in variants
    assert "plain" in templates
    assert variants == sorted(variants)


def test_special_logos():
    special = special_logos()
    assert "silhouette-current-color" in special
    assert special == sorted(special)
    for name in special:
        assert special_logo_path(name).is_file()


def test_special_logo_path_missing_raises():
    with pytest.raises(ValueError):
        special_logo_path("not-a-logo")


def test_current_color_silhouette_takes_the_text_colour():
    """It is pasted inline, so it must use currentColor and carry no fixed fill."""
    svg = special_logo_path("silhouette-current-color").read_text(encoding="utf-8")
    assert 'fill="currentColor"' in svg
    assert "#" not in svg.split("<svg", 1)[1]  # no hex colours after the comment
    assert "<script" not in svg
