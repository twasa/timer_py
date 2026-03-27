uv run python `
    -m nuitka `
    --enable-plugin=tk-inter `
    --mode=onefile `
    --show-memory `
    --show-progress `
    --zig `
    --windows-console-mode=disable `
    --include-data-dir=audio=audio `
    --include-package=playsound3 `
    --include-package=_tkinter `
    --follow-imports `
    main.py
