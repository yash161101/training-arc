"""Draws the app icon (white tile, yellow blocks with an iron edge) as SVG and PNGs into public/icons."""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parents[2] / 'public' / 'icons'
TILE, BLOCK, EDGE = '#FFFFFF', '#FFC21A', '#1D1E21'
STEPS = [(28, 108), (68, 108), (68, 68), (108, 108), (108, 68), (108, 28)]


def svg(pad=0):
    size = 168 + 2 * pad
    blocks = ''.join(
        f'<rect x="{x}" y="{y}" width="32" height="32" fill="{BLOCK}" stroke="{EDGE}" stroke-width="4"/>'
        for x, y in STEPS)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad} {size} {size}">'
            f'<rect x="{-pad}" y="{-pad}" width="{size}" height="{size}" fill="{TILE}"/>{blocks}</svg>')


def main():
    (OUT / 'icon.svg').write_text(svg())
    jobs = [('icon-192.png', 192, 0), ('icon-512.png', 512, 0), ('apple-touch-icon.png', 180, 0),
            ('icon-maskable-512.png', 512, 24)]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        for name, px, pad in jobs:
            page = b.new_page(viewport={'width': px, 'height': px})
            page.set_content(f'<html><body style="margin:0">{svg(pad).replace("<svg ", f"<svg width=\"{px}\" height=\"{px}\" ", 1)}</body></html>')
            page.screenshot(path=str(OUT / name), omit_background=False)
            page.close()
        b.close()


if __name__ == '__main__':
    main()
