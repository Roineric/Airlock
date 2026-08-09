# Airlock icon creation and replacement guide

This guide explains how to design an Airlock icon, convert it into a proper
Windows icon, display it in the Tkinter window, and embed it into the packaged
`Airlock.exe`.

## 1. Understand the two icons

Windows applications effectively have two related icon locations:

1. **Executable icon** — shown for `Airlock.exe` in File Explorer, shortcuts,
   and some Windows security dialogs.
2. **Window icon** — shown in the Airlock title bar, taskbar, and window switcher.

PyInstaller's `--icon` option handles the executable icon. Tkinter's
`root.iconbitmap()` handles the window icon. For a consistent result, configure
both with the same `.ico` file.

## 2. Choose a visual idea

Airlock is a transition tool rather than a security or password application.
The icon should communicate “leaving work mode” or “closing a session” without
looking like antivirus software.

### Recommended concept: transition hatch

A strong concept for Airlock would be:

- a simple circular airlock hatch;
- a small opening or doorway in its center;
- cool blue or teal on the work side;
- a warm amber light, crescent, or star on the off-duty side;
- a dark navy background or outline;
- no words or tiny lettering.

This combines the literal airlock image with the app's real purpose: moving from
work mode into personal time.

### Other suitable concepts

- **Closing hatch:** a circular mechanical door with one bold handle.
- **Work-to-rest transition:** a small briefcase on one side and a crescent moon
  on the other, separated by a doorway.
- **Quiet mode:** a speech bubble passing through a closing circular gate.
- **Session boundary:** two colored zones connected by a narrow transition door.
- **Minimal lettermark:** a geometric `A` shaped like an open doorway.
- **Power-down ritual:** a simplified sunset behind a closing hatch.

Avoid a plain padlock unless the project is meant to look like a security tool.
“Airlock” can easily be mistaken for encryption, access control, or antivirus
software if the icon is only a conventional lock.

## 3. Design for small sizes first

Windows may display the icon at only 16 × 16 pixels. Details that look attractive
at 1024 × 1024 can become visual noise when reduced.

Use these rules:

- Start with a square canvas.
- Use one central symbol and a simple silhouette.
- Use two or three main colors.
- Prefer thick shapes and generous spacing.
- Avoid text, thin lines, gradients with tiny transitions, and small decorations.
- Leave some transparent margin so the icon does not touch every edge.
- Test the design at 16, 24, 32, and 48 pixels before finalizing it.
- Make sure it remains recognizable on both light and dark Windows themes.

A good working master is a transparent 1024 × 1024 PNG. Keep that master even
after creating the `.ico`; it is easier to edit later.

## 4. Easiest ways to create the artwork

The methods below are ordered approximately from easiest to most controlled.

### Option A: generate a draft with an image generator

This is the quickest way to explore several visual directions.

Example prompt:

```text
Create a clean Windows desktop app icon for an application called Airlock.
The app closes work communication apps and marks the transition into off-duty
time. Show a minimal circular airlock hatch opening toward a small warm sunset
or crescent. Dark navy, teal, and one amber accent. Bold geometric shapes,
centered composition, transparent background, no text, no letters, no mockup,
no shadows outside the icon, readable at 16 pixels, square 1024 × 1024 image.
```

Useful prompt variations:

- Replace the crescent with a small star.
- Ask for a flat vector-like style.
- Ask for a Windows 11-style fluent icon.
- Ask for a monochrome version for maximum clarity.
- Generate four concept variations before selecting one.

AI output usually needs cleanup. Inspect the hatch geometry, remove accidental
text, simplify tiny details, and verify transparency. Keep the final design
original and avoid asking for another product's trademarked visual style.

### Option B: build it from simple shapes in PowerPoint

PowerPoint is surprisingly practical for a simple icon:

1. Create a blank slide.
2. Set a square slide or draw inside a square guide.
3. Use circles, rounded rectangles, arcs, and triangles.
4. Align everything with **Align Center** and **Align Middle**.
5. Use thick fills instead of thin outlines.
6. Group the finished shapes.
7. Right-click the group and choose **Save as Picture**.
8. Export a PNG, preferably with a transparent background if your version and
   workflow support it.

This method is good for the circular hatch, doorway, moon, and simple geometric
lettermark concepts.

### Option C: use a browser-based design editor

Canva, Figma, Photopea, or another browser-based editor can build the icon from
basic vector shapes. Use a 1024 × 1024 canvas, keep the design centered, and
export a transparent PNG.

Before uploading project artwork to an online service, consider whether the
design is private or commercially sensitive. Airlock's current personal MVP icon
is low-risk, but local tools avoid that issue entirely.

### Option D: use Inkscape

Inkscape is a strong free option when you want editable vector artwork:

1. Create a 1024 × 1024 document.
2. Draw the design with circles and Bézier shapes.
3. Keep elements on separate layers or groups.
4. Save the editable master as `assets/airlock-icon.svg`.
5. Export a transparent 1024 × 1024 PNG as
   `assets/airlock-icon-master.png`.

SVG is ideal as the long-term design source because it can be resized without
losing sharpness. Tkinter and Windows packaging will still use the converted
`.ico` file.

### Option E: draw it manually in a raster editor

GIMP, Krita, Affinity Photo, or Photoshop provide precise pixel-level control.
Create the master at 1024 × 1024 with transparency, but repeatedly preview it at
small sizes. A manually refined 32 × 32 or 16 × 16 layer can improve clarity if
automatic scaling becomes blurry.

## 5. Add the source artwork to the repository

Use this structure:

```text
assets/
├── airlock-icon-master.png
├── airlock-icon.svg          # optional editable vector master
└── airlock.ico               # Windows application icon
```

Only `airlock.ico` is required by the program. The PNG and SVG are useful source
assets and should be preserved so the design can be changed later.

Do not replace the current executable yet. First inspect the image at several
sizes and keep the existing `dist/Airlock.exe` until the new build succeeds.

## 6. Convert the artwork into a real multi-size ICO

Renaming a PNG from `.png` to `.ico` does not create a valid Windows icon. An ICO
is a container that can hold several image sizes.

Recommended embedded sizes:

```text
16 × 16
24 × 24
32 × 32
48 × 48
64 × 64
128 × 128
256 × 256
```

### Conversion method A: ImageMagick

After installing ImageMagick, run from the repository root:

```powershell
magick assets\airlock-icon-master.png `
  -define icon:auto-resize=256,128,64,48,32,24,16 `
  assets\airlock.ico
```

This creates a multi-resolution ICO from the master PNG.

### Conversion method B: Pillow

Install Pillow in the virtual environment:

```powershell
.\.venv\Scripts\python.exe -m pip install Pillow
```

Use this one-time conversion script from PowerShell:

```powershell
@'
from pathlib import Path
from PIL import Image

source = Path("assets/airlock-icon-master.png")
destination = Path("assets/airlock.ico")

image = Image.open(source).convert("RGBA")
if image.width != image.height:
    raise ValueError("The icon master must be square.")

image.save(
    destination,
    format="ICO",
    sizes=[
        (16, 16),
        (24, 24),
        (32, 32),
        (48, 48),
        (64, 64),
        (128, 128),
        (256, 256),
    ],
)
print(f"Created {destination}")
'@ | .\.venv\Scripts\python.exe -
```

Pillow is needed only for conversion unless the script is added permanently to
the project. Airlock itself does not need Pillow at runtime.

### Conversion method C: an online ICO converter

This is the easiest no-install method:

1. Upload the transparent square PNG.
2. Select multiple Windows sizes, including 16, 32, 48, and 256 pixels.
3. Download the generated ICO.
4. Rename it to `airlock.ico`.
5. Place it under `assets/`.

Use a reputable converter and avoid uploading artwork that must remain private.

## 7. Make the icon work from source and from PyInstaller

PyInstaller extracts a one-file application into a temporary directory at
runtime. A normal repository-relative path therefore does not work in both
development and packaged modes. Add a small resource-path helper to
`src/airlock/gui.py`.

Add `sys` to the imports:

```python
import sys
```

Add this function near the module constants:

```python
def resource_path(relative_path: str) -> Path:
    """Return an asset path in source and PyInstaller builds."""
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parents[2]

    return base_path / relative_path
```

Why it works:

- From source, `gui.py` is under `src/airlock`, so `parents[2]` is the repository
  root.
- In a PyInstaller one-file build, `sys._MEIPASS` is the temporary directory
  containing bundled data files.

Then update `main()` immediately after creating the Tk root:

```python
def main() -> None:
    root = tk.Tk()
    try:
        root.iconbitmap(default=str(resource_path("assets/airlock.ico")))
    except tk.TclError:
        pass

    # Existing settings-loading code continues here.
```

The `TclError` guard prevents a missing or invalid icon from making Airlock
unusable. During development, it may be preferable to show or log that error
instead of silently ignoring it; the minimal MVP currently has no logging
system.

## 8. Test the icon from source

Run:

```powershell
.\.venv\Scripts\python.exe -m airlock
```

Check:

- The Airlock title bar uses the new icon.
- The taskbar button uses the new icon.
- The icon remains clear when the taskbar uses small buttons.
- The window still opens if the icon file is temporarily unavailable.
- No console window appears when running the packaged version later.

Also run the automated tests:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

The icon change should not affect process safety or settings behavior.

## 9. Rebuild the executable with the icon

Use PyInstaller's `--icon` option for the executable and `--add-data` so Tkinter
can load the same ICO at runtime:

```powershell
.\.venv\Scripts\python.exe -m PyInstaller `
  --noconfirm `
  --clean `
  --onefile `
  --windowed `
  --name Airlock `
  --paths src `
  --icon assets\airlock.ico `
  --add-data "assets\airlock.ico:assets" `
  src\airlock\__main__.py
```

Then copy the external settings file beside the executable:

```powershell
Copy-Item airlock_settings.json dist\airlock_settings.json -Force
```

The results are:

```text
dist/
├── Airlock.exe
└── airlock_settings.json
```

The options have different jobs:

- `--icon assets\airlock.ico` embeds the Explorer/executable icon.
- `--add-data "assets\airlock.ico:assets"` bundles the file so Tkinter can load
  it inside the one-file application.
- `root.iconbitmap(...)` assigns it to the actual Tk window.

PyInstaller's official documentation describes `--icon`, `--add-data`,
`--onefile`, and `--windowed` in its
[usage guide](https://pyinstaller.org/en/stable/usage.html).

## 10. Verify the packaged result safely

Launch from the distribution directory:

```powershell
Set-Location dist
.\Airlock.exe
```

Do not press End Workday merely to test the icon. Confirm only:

- The window opens.
- The title bar and taskbar show the intended icon.
- File Explorer shows the intended icon for `Airlock.exe`.
- `airlock_settings.json` is found and the preview loads.
- Closing the window exits Airlock normally.

After visual verification, run the source tests again if the build process or
source code was changed.

## 11. Windows still shows the old icon

Windows Explorer caches icons aggressively. A correct rebuild can temporarily
appear to retain the old icon.

Try these steps in order:

1. Confirm the PyInstaller command included `--clean` and `--icon`.
2. Delete or move the previous `dist/Airlock.exe` before rebuilding.
3. Give the rebuilt executable a temporary name such as `Airlock-new.exe`.
4. Refresh File Explorer or open a different directory and return.
5. Unpin the old taskbar shortcut and pin the rebuilt executable again.
6. Remove and recreate any desktop shortcut.
7. Restart Windows Explorer or sign out and back in if the cache persists.

Do not assume the ICO is broken merely because one old shortcut retains a cached
image. Check the newly built executable under a new filename first.

## 12. Quality checklist

Before accepting the icon, confirm:

- [ ] The master artwork is square and high resolution.
- [ ] The icon contains no accidental text or AI artifacts.
- [ ] The silhouette remains recognizable at 16 × 16.
- [ ] It looks acceptable on light and dark backgrounds.
- [ ] `assets/airlock.ico` contains multiple resolutions.
- [ ] The source application shows the icon.
- [ ] `Airlock.exe` shows the icon in Explorer.
- [ ] The packaged window and taskbar show the icon.
- [ ] The settings file remains beside the executable.
- [ ] Automated tests still pass.
- [ ] The rebuilt executable receives a new SHA-256 hash in the handoff notes.

## Recommended first attempt

For the fastest path with a good chance of success:

1. Generate or draw a flat circular hatch with a teal body and amber crescent.
2. Export a transparent 1024 × 1024 PNG.
3. Simplify it until it remains readable at 16 × 16.
4. Convert it to a multi-size ICO with Pillow or ImageMagick.
5. Save it as `assets/airlock.ico`.
6. Add the resource-path helper and `root.iconbitmap()` call.
7. Rebuild with both `--icon` and `--add-data`.
8. Verify source, Explorer, title-bar, and taskbar appearances separately.

Once a candidate image exists, the remaining code and packaging changes are
small and can be implemented and tested without changing Airlock's process
closure behavior.
