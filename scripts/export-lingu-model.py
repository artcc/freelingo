"""Derive the reusable web GLB without changing Blender sources or mesh geometry.

Keep all clips, omit tracks identical to the node's rest transform, and repack
only referenced buffers. No Blender installation or third-party package is needed.
"""

import copy
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    source = (ROOT / "blender/lingu.glb").read_bytes()
    json_size, _ = struct.unpack_from("<II", source, 12)
    document = json.loads(source[20 : 20 + json_size])
    binary_size, _ = struct.unpack_from("<II", source, 20 + json_size)
    binary = source[28 + json_size : 28 + json_size + binary_size]
    accessors = document["accessors"]
    views = document["bufferViews"]

    def rest_track(channel: dict, sampler: dict) -> bool:
        target = channel["target"]
        default = {"translation": [0, 0, 0], "rotation": [0, 0, 0, 1], "scale": [1, 1, 1]}
        if target["path"] not in default:
            return False
        node = document["nodes"][target["node"]]
        if "matrix" in node or sampler.get("interpolation") == "CUBICSPLINE":
            return False
        accessor = accessors[sampler["output"]]
        if accessor["componentType"] != 5126 or "sparse" in accessor:
            return False
        expected = node.get(target["path"], default[target["path"]])
        view = views[accessor["bufferView"]]
        stride = view.get("byteStride", len(expected) * 4)
        offset = view.get("byteOffset", 0) + accessor.get("byteOffset", 0)
        for index in range(accessor["count"]):
            values = struct.unpack_from(f"<{len(expected)}f", binary, offset + index * stride)
            if any(abs(value - rest) > 1e-7 for value, rest in zip(values, expected, strict=True)):
                return False
        return True

    animations = []
    for original in document["animations"]:
        animation = {"name": original["name"], "channels": [], "samplers": []}
        for channel in original["channels"]:
            sampler = original["samplers"][channel["sampler"]]
            if rest_track(channel, sampler):
                continue
            channel = copy.deepcopy(channel)
            channel["sampler"] = len(animation["samplers"])
            animation["channels"].append(channel)
            animation["samplers"].append(copy.deepcopy(sampler))
        animations.append(animation)
    document["animations"] = animations

    kept_accessors = []
    kept_views = []
    packed = bytearray()
    accessor_map = {}
    view_map = {}

    def keep_accessor(index: int) -> int:
        if index in accessor_map:
            return accessor_map[index]
        accessor = copy.deepcopy(accessors[index])
        if "sparse" in accessor:
            raise ValueError("Sparse accessors need an explicit export path")
        view_index = accessor["bufferView"]
        if view_index not in view_map:
            view = copy.deepcopy(views[view_index])
            packed.extend(b"\0" * (-len(packed) % 4))
            offset = view.get("byteOffset", 0)
            chunk = binary[offset : offset + view["byteLength"]]
            view["byteOffset"] = len(packed)
            view["buffer"] = 0
            packed.extend(chunk)
            view_map[view_index] = len(kept_views)
            kept_views.append(view)
        accessor["bufferView"] = view_map[view_index]
        accessor_map[index] = len(kept_accessors)
        kept_accessors.append(accessor)
        return accessor_map[index]

    for mesh in document["meshes"]:
        for primitive in mesh["primitives"]:
            primitive["attributes"] = {
                key: keep_accessor(value) for key, value in primitive["attributes"].items()
            }
            if "indices" in primitive:
                primitive["indices"] = keep_accessor(primitive["indices"])
            for target in primitive.get("targets", []):
                for key, value in target.items():
                    target[key] = keep_accessor(value)
    for skin in document.get("skins", []):
        if "inverseBindMatrices" in skin:
            skin["inverseBindMatrices"] = keep_accessor(skin["inverseBindMatrices"])
    for animation in animations:
        for sampler in animation["samplers"]:
            sampler["input"] = keep_accessor(sampler["input"])
            sampler["output"] = keep_accessor(sampler["output"])

    document["accessors"] = kept_accessors
    document["bufferViews"] = kept_views
    document["buffers"] = [{"byteLength": len(packed)}]
    document["asset"]["generator"] = "FreeLingo Lingu web export"
    encoded = json.dumps(document, separators=(",", ":"), ensure_ascii=False).encode()
    encoded += b" " * (-len(encoded) % 4)
    packed.extend(b"\0" * (-len(packed) % 4))
    result = (
        struct.pack("<III", 0x46546C67, 2, 28 + len(encoded) + len(packed))
        + struct.pack("<II", len(encoded), 0x4E4F534A)
        + encoded
        + struct.pack("<II", len(packed), 0x004E4942)
        + packed
    )
    destination = ROOT / "frontend/public/models/lingu.glb"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(result)
    print(f"Lingu GLB: {len(source):,} → {len(result):,} bytes; {len(animations)} clips")


if __name__ == "__main__":
    main()
