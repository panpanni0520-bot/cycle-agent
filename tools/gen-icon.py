#!/usr/bin/env python3
"""生成 App 图标：纯色底 + 周期环 + 状态圆点。用法: python3 tools/gen-icon.py <输出目录>"""
import zlib, struct, math, sys

BG = (124, 74, 103)       # 主色 plum #7C4A67
RING = (243, 230, 238)    # 浅 #F3E6EE
DOT = (250, 246, 244)

def make(path, size):
    cx = cy = size / 2
    ring_r = size * 0.30
    ring_w = size * 0.048
    dot_r = size * 0.075
    ang = math.radians(-50)
    dx, dy = cx + ring_r * math.cos(ang), cy + ring_r * math.sin(ang)
    rows = []
    for y in range(size):
        row = bytearray()
        for x in range(size):
            d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
            dd = math.hypot(x + 0.5 - dx, y + 0.5 - dy)
            if dd <= dot_r:
                row += bytes(DOT)
            elif abs(d - ring_r) <= ring_w / 2:
                row += bytes(RING)
            else:
                row += bytes(BG)
        rows.append(b"\x00" + bytes(row))
    raw = b"".join(rows)
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9))
           + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)
    print(path, size)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    make(out + "/apple-touch-icon.png", 180)
    make(out + "/icon-192.png", 192)
    make(out + "/icon-512.png", 512)
