# Toolbox

TUI app quản lý các tool convert mini trong máy.

## Tools có sẵn

- **convertPdf** — Convert DOCX → PDF (dùng LibreOffice)
- **convert9to16** — Pad ảnh sang khung 16:9
- **convert16to9** — Pad ảnh sang khung 9:16

## Chạy app

```bash
uv run --with textual python3 toolbox.py
```

## Tính năng

- Xem hướng dẫn từng tool
- Chạy `--help` của tool để xem chi tiết
- Điều hướng bằng bàn phím: `j`/`k` hoặc `↑`/`↓`
- Màu Catppuccin Mocha theme

## Layout

```
┌─────────────────┬────────────────────────────────┐
│  📦 Tools       │  convertPdf                    │
│  ✅ convertPdf  │  Convert DOCX → PDF            │
│  ✅ convert9to16│                                │
│  ✅ convert16to9│  Ví dụ:                        │
│                 │    $ convertPdf /path          │
│                 │                                │
│                 │  --help output:                │
│                 │    Sử dụng: convertPdf...     │
└─────────────────┴────────────────────────────────┘
```