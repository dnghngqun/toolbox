#!/usr/bin/env python3
"""Toolbox - TUI app quản lý các tool convert mini."""

import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from typing import ClassVar

try:
    from textual.app import App, ComposeResult
    from textual.binding import Binding
    from textual.containers import Horizontal, Vertical
    from textual.widgets import Button, Footer, Header, Static
except ImportError:
    print("Lỗi: Cần cài textual: uv run --with textual python3 toolbox.py")
    sys.exit(1)


@dataclass
class ToolInfo:
    command: str
    title: str
    summary: str
    examples: list[str] = field(default_factory=list)
    command_path: str = ""


def get_command_path(cmd: str) -> str:
    p = shutil.which(cmd)
    return p if p else "Không tìm thấy trong PATH"


TOOLS: list[ToolInfo] = [
    ToolInfo(
        command="convertPdf",
        title="convertPdf",
        summary="Convert toàn bộ file .docx trong một thư mục sang PDF bằng LibreOffice.",
        examples=[
            "convertPdf",
            "convertPdf /duong/dan/thu-muc-docx",
            "convertPdf --batch /duong/dan/thu-muc-docx",
        ],
    ),
    ToolInfo(
        command="convert9to16",
        title="convert9to16",
        summary="Pad ảnh trong thư mục sang khung ngang 16:9 (thêm nền).",
        examples=[
            "convert9to16 /duong/dan/thu-muc-anh",
            "convert9to16 /duong/dan/thu-muc-anh --hexcolor '#222222'",
        ],
    ),
    ToolInfo(
        command="convert16to9",
        title="convert16to9",
        summary="Pad ảnh trong thư mục sang khung dọc 9:16 (thêm nền).",
        examples=[
            "convert16to9 /duong/dan/thu-muc-anh",
            "convert16to9 /duong/dan/thu-muc-anh --hexcolor '#222222'",
        ],
    ),
]


def get_help_text(command: str) -> str:
    path = shutil.which(command)
    if not path:
        return f"Lệnh '{command}' không tìm thấy trong PATH."

    try:
        result = subprocess.run(
            [path, "--help"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.stdout.strip() or result.stderr.strip() or "(Không có nội dung --help)"
    except subprocess.TimeoutExpired:
        return "(Timeout khi lấy help)"
    except Exception as e:
        return f"(Lỗi: {e})"


class ToolboxApp(App):
    CSS = """
    Screen {
        background: #1e1e2e;
        color: #cdd6f4;
    }

    #sidebar {
        width: 26;
        background: #181825;
        border-right: solid #313244;
    }

    #tool-list {
        height: 1fr;
        padding: 4;
    }

    #tool-list Button {
        width: 100%;
        height: 3;
        margin-bottom: 2;
        background: #313244;
        border: solid #45475a;
    }

    #tool-list Button.active-tool {
        background: #89b4fa;
        color: #1e1e2e;
    }

    #content-area {
        width: 1fr;
        padding: 4 8;
    }

    #tool-summary {
        color: #cba6f7;
        margin-bottom: 2;
    }

    #tool-path {
        color: #6c7086;
        margin-bottom: 6;
    }

    #examples-label {
        color: #f9e2af;
        margin-top: 4;
        margin-bottom: 2;
    }

    #help-label {
        color: #f9e2af;
        margin-top: 6;
        margin-bottom: 2;
    }

    #example-item {
        color: #a6e3a1;
    }

    #help-content {
        color: #a6adc8;
    }

    #hint-bar {
        height: 3;
        background: #181825;
        color: #6c7086;
        padding: 0 4;
        border-top: solid #313244;
    }
    """

    TITLE = "Toolbox"
    BINDINGS: ClassVar[list[Binding]] = [
        Binding("q", "quit", "Thoát"),
        Binding("j", "select_next", "Tool tiếp", show=False),
        Binding("k", "select_prev", "Tool trước", show=False),
        Binding("r", "refresh", "Làm mới", show=False),
    ]

    def __init__(self):
        super().__init__()
        self.selected_index = 0
        for t in TOOLS:
            t.command_path = get_command_path(t.command)

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Static("[b]📦 Tools[/b]", id="sidebar-title")
                with Vertical(id="tool-list"):
                    for i, tool in enumerate(TOOLS):
                        icon = "✅" if tool.command_path != "Không tìm thấy trong PATH" else "❌"
                        yield Button(f"{icon} {tool.title}", id=f"btn-{i}")
            with Vertical(id="content-area"):
                pass
        yield Footer()

    def on_mount(self) -> None:
        self.select_tool(0)

    def select_tool(self, index: int) -> None:
        if index < 0 or index >= len(TOOLS):
            return
        self.selected_index = index

        # Update buttons
        for i in range(len(TOOLS)):
            btn = self.query_one(f"#btn-{i}", Button)
            btn.remove_class("active-tool")
        self.query_one(f"#btn-{index}", Button).add_class("active-tool")

        # Update content
        tool = TOOLS[index]
        help_text = get_help_text(tool.command)

        area = self.query_one("#content-area", Vertical)
        area.remove_children()

        area.mount(Static(f"[b]{tool.title}[/b] — {tool.summary}", id="tool-summary"))
        area.mount(Static(f"Đường dẫn: [dim]{tool.command_path}[/dim]", id="tool-path"))
        area.mount(Static("Ví dụ sử dụng:", id="examples-label"))
        for i, ex in enumerate(tool.examples):
            area.mount(Static(f"  [cyan]$[/cyan] {ex}", id=f"example-item-{i}"))
        area.mount(Static("Nội dung --help:", id="help-label"))
        area.mount(Static(help_text, id="help-content", markup=False))

    def action_select_next(self) -> None:
        self.select_tool((self.selected_index + 1) % len(TOOLS))

    def action_select_prev(self) -> None:
        self.select_tool((self.selected_index - 1) % len(TOOLS))

    def action_refresh(self) -> None:
        self.select_tool(self.selected_index)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        idx = int(event.button.id.replace("btn-", ""))
        self.select_tool(idx)


if __name__ == "__main__":
    app = ToolboxApp()
    app.run()