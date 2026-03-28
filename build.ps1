uv run python `
    -m nuitka `
    --enable-plugin=tk-inter `
    --mode=standalone `
    --output-dir=dist `
    --windows-console-mode=disable `
    --include-data-dir=audio=audio `
    --include-package=playsound3 `
    main.py
