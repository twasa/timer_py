uv run python `
    -m nuitka `
    --enable-plugin=tk-inter `
    --mode=onefile `
    --show-memory `
    --show-progress `
    --zig `
    --include-data-dir=audio=audio main.py
