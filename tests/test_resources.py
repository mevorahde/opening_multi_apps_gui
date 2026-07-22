from __future__ import annotations

import struct
import zlib
from importlib import resources
from pathlib import Path

import pytest

from morning_app_launcher import app

RESOURCE_PACKAGE = "morning_app_launcher.resources"
PNG_NAME = "morning-app-launcher.png"
ICO_NAME = "morning-app-launcher.ico"
REQUIRED_ICO_SIZES = {16, 24, 32, 48, 64, 128, 256}


class FakeRoot:
    def __init__(self, *, reject_ico: bool = False) -> None:
        self.reject_ico = reject_ico
        self.iconbitmap_calls: list[str] = []
        self.iconphoto_calls: list[tuple[bool, object]] = []
        self._morning_app_launcher_icon: object | None = None

    def iconbitmap(self, *, default: str) -> None:
        self.iconbitmap_calls.append(default)
        if self.reject_ico:
            raise RuntimeError("simulated ICO failure")

    def iconphoto(self, default: bool, image: object) -> None:
        self.iconphoto_calls.append((default, image))


def _resource_bytes(name: str) -> bytes:
    return resources.files(RESOURCE_PACKAGE).joinpath(name).read_bytes()


def _png_corner_alpha(data: bytes) -> tuple[int, int, int, int]:
    width, height, bit_depth, color_type = struct.unpack(">IIBB", data[16:26])
    assert bit_depth == 8
    assert color_type == 6
    position = 8
    compressed = bytearray()
    while position < len(data):
        length = struct.unpack(">I", data[position : position + 4])[0]
        chunk_type = data[position + 4 : position + 8]
        chunk_data = data[position + 8 : position + 8 + length]
        if chunk_type == b"IDAT":
            compressed.extend(chunk_data)
        position += 12 + length

    raw = zlib.decompress(compressed)
    stride = width * 4
    rows: list[bytearray] = []
    offset = 0
    for _row_number in range(height):
        filter_type = raw[offset]
        scanline = bytearray(raw[offset + 1 : offset + 1 + stride])
        previous = rows[-1] if rows else bytearray(stride)
        for index in range(stride):
            left = scanline[index - 4] if index >= 4 else 0
            above = previous[index]
            upper_left = previous[index - 4] if index >= 4 else 0
            if filter_type == 1:
                scanline[index] = (scanline[index] + left) & 0xFF
            elif filter_type == 2:
                scanline[index] = (scanline[index] + above) & 0xFF
            elif filter_type == 3:
                scanline[index] = (scanline[index] + ((left + above) // 2)) & 0xFF
            elif filter_type == 4:
                estimate = left + above - upper_left
                distances = (
                    abs(estimate - left),
                    abs(estimate - above),
                    abs(estimate - upper_left),
                )
                predictor = (left, above, upper_left)[distances.index(min(distances))]
                scanline[index] = (scanline[index] + predictor) & 0xFF
            elif filter_type != 0:
                raise AssertionError(f"Unsupported PNG filter: {filter_type}")
        rows.append(scanline)
        offset += stride + 1

    return (rows[0][3], rows[0][-1], rows[-1][3], rows[-1][-1])


def test_final_icon_resources_replace_old_favicon() -> None:
    resource_root = resources.files(RESOURCE_PACKAGE)

    assert resource_root.joinpath(PNG_NAME).is_file()
    assert resource_root.joinpath(ICO_NAME).is_file()
    assert not resource_root.joinpath("favicon.ico").is_file()


def test_png_has_rgba_pixels_and_transparent_corners() -> None:
    data = _resource_bytes(PNG_NAME)

    assert data.startswith(b"\x89PNG\r\n\x1a\n")
    assert data[25] == 6
    assert _png_corner_alpha(data) == (0, 0, 0, 0)


def test_ico_contains_exact_required_sizes() -> None:
    data = _resource_bytes(ICO_NAME)
    reserved, image_type, count = struct.unpack("<HHH", data[:6])
    entries = [
        struct.unpack("<BBBBHHII", data[6 + index * 16 : 22 + index * 16])
        for index in range(count)
    ]
    sizes = {(width or 256, height or 256) for width, height, *_rest in entries}

    assert (reserved, image_type) == (0, 1)
    assert count == len(REQUIRED_ICO_SIZES)
    assert sizes == {(size, size) for size in REQUIRED_ICO_SIZES}


def test_windows_prefers_ico(monkeypatch: pytest.MonkeyPatch) -> None:
    root = FakeRoot()

    def reject_photo_image(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("PNG fallback should not be used when ICO loading succeeds.")

    monkeypatch.setattr(app.os, "name", "nt")
    monkeypatch.setattr(app.tk, "PhotoImage", reject_photo_image)

    app._apply_icon(root)  # type: ignore[arg-type]

    assert len(root.iconbitmap_calls) == 1
    assert Path(root.iconbitmap_calls[0]).name == ICO_NAME
    assert root.iconphoto_calls == []


def test_png_fallback_retains_photo_reference(monkeypatch: pytest.MonkeyPatch) -> None:
    root = FakeRoot(reject_ico=True)
    photo = object()

    def fake_photo_image(*_args: object, **_kwargs: object) -> object:
        return photo

    monkeypatch.setattr(app.os, "name", "nt")
    monkeypatch.setattr(app.tk, "PhotoImage", fake_photo_image)

    app._apply_icon(root)  # type: ignore[arg-type]

    assert root.iconphoto_calls == [(True, photo)]
    assert root._morning_app_launcher_icon is photo


def test_icon_loading_failure_is_nonfatal(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_to_find_resources(_package: str) -> None:
        raise RuntimeError("simulated resource failure")

    monkeypatch.setattr(app.resources, "files", fail_to_find_resources)

    app._apply_icon(object())  # type: ignore[arg-type]
