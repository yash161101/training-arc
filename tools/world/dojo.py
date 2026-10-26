import sys
from build import defs, pts

W, H = 900, 1200
BX0, BX1, BY0, BY1 = 190, 710, 300, 700

def lw(t, h):
    x = BX0 * t
    top = BY0 * t
    bot = H - (H - BY1) * t
    return (x, bot + (top - bot) * h)

def rw(t, h):
    x = W - (W - BX1) * t
    top = BY0 * t
    bot = H - (H - BY1) * t
    return (x, bot + (top - bot) * h)

def fl(u, t):
    hw = 450 - (450 - (BX1 - BX0) / 2) * t
    return (450 + u * hw, H - (H - BY1) * t)

def quad(a, b, c, d, fill, extra=''):
    return f'<polygon points="{pts([a, b, c, d])}" fill="{fill}" {extra}/>'

def scene():
    s = ['<defs><linearGradient id="dfloor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8A5E3E"/><stop offset="1" stop-color="#B07C52"/></linearGradient>'
         '<linearGradient id="dwallL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#CDBB98"/><stop offset="1" stop-color="#E3D5B8"/></linearGradient>'
         '<linearGradient id="dwallR" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#BFAE8C"/><stop offset="1" stop-color="#DCCDAF"/></linearGradient>'
         '<linearGradient id="dback" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EFE4CC"/><stop offset="1" stop-color="#E2D3B5"/></linearGradient>'
         '<linearGradient id="dceil" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4A2F1E"/><stop offset="1" stop-color="#6B4429"/></linearGradient>'
         '<linearGradient id="tatami" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C9C08A"/><stop offset="1" stop-color="#DCD39C"/></linearGradient>'
         '<linearGradient id="shoji" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF8E6"/><stop offset="1" stop-color="#F3E6C6"/></linearGradient>'
         '<linearGradient id="ray" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFF4D2" stop-opacity="0.55"/><stop offset="1" stop-color="#FFF4D2" stop-opacity="0"/></linearGradient>'
         '<linearGradient id="outside" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8FB9DD"/><stop offset="0.7" stop-color="#CFE0EA"/><stop offset="1" stop-color="#8DB262"/></linearGradient>'
         '<linearGradient id="bronze" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E2B866"/><stop offset="0.5" stop-color="#B9873A"/><stop offset="1" stop-color="#7E5622"/></linearGradient></defs>']
    s.append(quad((0, 0), (W, 0), (BX1, BY0), (BX0, BY0), 'url(#dceil)'))
    for t in (0.25, 0.5, 0.75):
        a, b = lw(t, 1), rw(t, 1)
        s.append(f'<rect x="{a[0]:.0f}" y="{a[1] - 10:.0f}" width="{b[0] - a[0]:.0f}" height="{14 + (1 - t) * 10:.0f}" fill="#3A2416"/>')
    for u in (-0.6, -0.2, 0.2, 0.6):
        x0 = 450 + u * 450
        x1 = 450 + u * (BX1 - BX0) / 2
        s.append(f'<path d="M{x0:.0f} 0 L{x1:.0f} {BY0}" stroke="#3A2416" stroke-width="6"/>')
    s.append(quad(lw(0, 1), lw(1, 1), lw(1, 0), lw(0, 0), 'url(#dwallL)'))
    s.append(quad(rw(0, 1), rw(1, 1), rw(1, 0), rw(0, 0), 'url(#dwallR)'))
    s.append(f'<rect x="{BX0}" y="{BY0}" width="{BX1 - BX0}" height="{BY1 - BY0}" fill="url(#dback)"/>')
    s.append(quad(fl(-1, 0), fl(1, 0), fl(1, 1), fl(-1, 1), 'url(#dfloor)'))
    for k in range(1, 12):
        u = -1 + k / 6
        a, b = fl(u, 0), fl(u, 1)
        s.append(f'<path d="M{a[0]:.0f} {a[1]:.0f} L{b[0]:.0f} {b[1]:.0f}" stroke="#6E4A30" stroke-width="1.5" opacity="0.6"/>')
    for t0, t1 in ((0.2, 0.45), (0.45, 0.7), (0.7, 0.92)):
        for u0, u1 in ((-0.55, 0), (0, 0.55)):
            s.append(quad(fl(u0, t0), fl(u1, t0), fl(u1, t1), fl(u0, t1), 'url(#tatami)', 'stroke="#3B4A2E" stroke-width="2"'))
    for x in (BX0, BX0 + 8, 330, 570, BX1 - 8):
        s.append(f'<rect x="{x}" y="{BY0}" width="8" height="{BY1 - BY0}" fill="#5E3920"/>')
    s.append(f'<rect x="{BX0}" y="{BY0}" width="{BX1 - BX0}" height="10" fill="#5E3920"/><rect x="{BX0}" y="{BY1 - 10}" width="{BX1 - BX0}" height="10" fill="#5E3920"/>')
    s.append(f'<rect x="206" y="320" width="116" height="360" fill="url(#shoji)"/>')
    s.append('<g stroke="#8A6A44" stroke-width="2">' + ''.join(f'<path d="M206 {y} H322"/>' for y in range(350, 680, 30)) + '<path d="M245 320 V680 M284 320 V680"/></g>')
    s.append('<rect x="342" y="330" width="216" height="360" fill="#CDBD99"/><rect x="342" y="330" width="216" height="14" fill="#5E3920"/><rect x="336" y="640" width="228" height="20" fill="#6B4429"/>')
    s.append('<rect x="392" y="352" width="116" height="270" fill="#F7EFDC"/><rect x="386" y="346" width="128" height="8" fill="#3A2416"/><rect x="386" y="620" width="128" height="8" fill="#3A2416"/><circle cx="390" cy="624" r="5" fill="#3A2416"/><circle cx="510" cy="624" r="5" fill="#3A2416"/>')
    for x, y in ((414, 520), (440, 520), (466, 520), (440, 494), (466, 494), (466, 468)):
        s.append(f'<rect x="{x}" y="{y}" width="22" height="22" fill="#1D1E21"/>')
    s.append('<rect x="414" y="560" width="74" height="4" fill="#1D1E21" opacity="0.7"/>')
    s.append('<rect x="430" y="612" width="40" height="28" fill="#4A2E1A"/><path d="M450 612 L450 590" stroke="#4A2E1A" stroke-width="2"/><ellipse cx="450" cy="586" rx="5" ry="8" fill="#FFC75A"/>')
    for bx in (350, 524):
        s.append(f'<path d="M{bx} 350 L{bx + 26} 350 L{bx + 26} 560 L{bx + 13} 548 L{bx} 560 Z" fill="#FFC21A"/><rect x="{bx - 2}" y="346" width="30" height="6" fill="#3A2416"/>')
    for i in range(6):
        x = 582 + i * 20
        s.append(f'<g class="d-plaque" data-i="{i}"><rect class="p-tag" x="{x}" y="360" width="14" height="70" stroke="#3A2416" stroke-width="2"/><circle cx="{x + 7}" cy="356" r="2.5" fill="#3A2416"/><g class="p-marks">' + ''.join(f'<rect x="{x + 4}" y="{372 + k * 16}" width="6" height="8" fill="#3A2416"/>' for k in range(3)) + '</g></g>')
    s.append('<rect x="578" y="346" width="124" height="6" fill="#3A2416"/>')
    s.append('<rect x="582" y="470" width="116" height="200" fill="url(#shoji)"/><g stroke="#8A6A44" stroke-width="2"><path d="M582 510 H698 M582 550 H698 M582 590 H698 M582 630 H698 M621 470 V670 M660 470 V670"/></g>')
    wa, wb, wc, wd = lw(0.18, 0.86), lw(0.62, 0.86), lw(0.62, 0.2), lw(0.18, 0.2)
    s.append(f'<clipPath id="win"><polygon points="{pts([wa, wb, wc, wd])}"/></clipPath><g clip-path="url(#win)">')
    s.append(quad(wa, wb, wc, wd, 'url(#outside)'))
    s.append(f'<polygon points="{wa[0] + 30:.0f},{wa[1] + 120:.0f} {wa[0] + 70:.0f},{wa[1] + 60:.0f} {wa[0] + 110:.0f},{wa[1] + 110:.0f} {wa[0] + 150:.0f},{wa[1] + 76:.0f} {wb[0]:.0f},{wb[1] + 70:.0f} {wc[0]:.0f},{wc[1] - 60:.0f} {wd[0]:.0f},{wd[1] - 80:.0f}" fill="#8EA6C2"/>')
    s.append(f'<rect x="{wa[0] + 40:.0f}" y="{wa[1] + 90:.0f}" width="16" height="{(wd[1] - wa[1]) - 160:.0f}" fill="#F4FBFD" opacity="0.9"/>')
    s.append(f'<polygon points="{wd[0]:.0f},{wd[1] - 70:.0f} {wc[0]:.0f},{wc[1] - 40:.0f} {wc[0]:.0f},{wc[1]:.0f} {wd[0]:.0f},{wd[1]:.0f}" fill="#7DA463"/>')
    s.append('</g>')
    s.append(f'<polygon points="{pts([wa, wb, wc, wd])}" fill="none" stroke="#5E3920" stroke-width="10"/>')
    mid = ((wa[0] + wb[0]) / 2, (wa[1] + wb[1]) / 2), ((wd[0] + wc[0]) / 2, (wd[1] + wc[1]) / 2)
    s.append(f'<path d="M{mid[0][0]:.0f} {mid[0][1]:.0f} L{mid[1][0]:.0f} {mid[1][1]:.0f}" stroke="#5E3920" stroke-width="6"/>')
    if True:
        s.append(f'<polygon id="d-ray" points="{wa[0]:.0f},{wa[1]:.0f} {wb[0]:.0f},{wb[1]:.0f} {fl(0.4, 0.55)[0]:.0f},{fl(0.4, 0.55)[1]:.0f} {fl(-0.3, 0.05)[0]:.0f},{fl(-0.3, 0.05)[1]:.0f}" fill="url(#ray)"/>')
    r0, r1 = rw(0.1, 0.84), rw(0.86, 0.84)
    s.append(f'<path d="M{r0[0]:.0f} {r0[1]:.0f} L{r1[0]:.0f} {r1[1]:.0f}" stroke="#3A2416" stroke-width="5"/>')
    ro = [0.15, 0.27, 0.39, 0.51, 0.63, 0.75]
    for idx, t in enumerate(ro):
        top = rw(t, 0.83)
        bot = rw(t + 0.06, 0.42)
        x0 = top[0] - 4
        w = 30 - t * 14
        marks = ''.join(f'<rect class="m" data-k="{k}" x="{x0 - w / 2 - w * 0.18:.0f}" y="{top[1] + 10 + k * (w * 0.5):.0f}" width="{w * 0.36:.0f}" height="{w * 0.36:.0f}" fill="#FFC21A" stroke="#3A2416" stroke-width="1"/>' for k in range(5))
        s.append(f'<g class="d-scroll" data-i="{idx}"><g class="sc-open"><rect x="{x0 - w:.0f}" y="{top[1]:.0f}" width="{w:.0f}" height="{bot[1] - top[1]:.0f}" fill="#F7EFDC" stroke="#3A2416" stroke-width="1.5"/>'
                 f'<rect x="{x0 - w - 3:.0f}" y="{top[1] - 4:.0f}" width="{w + 6:.0f}" height="5" fill="#3A2416"/><rect x="{x0 - w - 3:.0f}" y="{bot[1]:.0f}" width="{w + 6:.0f}" height="5" fill="#3A2416"/>{marks}</g>'
                 f'<g class="sc-rolled"><rect x="{x0 - w:.0f}" y="{top[1] - 2:.0f}" width="{w:.0f}" height="{w * 0.45:.0f}" rx="{w * 0.22:.0f}" fill="#E9DCC0" stroke="#3A2416" stroke-width="1.5"/><rect x="{x0 - w - 3:.0f}" y="{top[1] - 4:.0f}" width="{w + 6:.0f}" height="4" fill="#3A2416"/></g></g>')
    for (lx, ly, sc) in ((300, 150, 1.0), (600, 150, 1.0), (450, 250, 0.7)):
        s.append(f'<g transform="translate({lx} {ly}) scale({sc})"><path d="M0 -150 L0 -6" stroke="#3A2416" stroke-width="2"/><rect x="-22" y="-6" width="44" height="58" rx="18" fill="#F2B33D"/><path d="M-22 12 H22 M-22 30 H22" stroke="#C9851B" stroke-width="2"/><rect x="-12" y="-10" width="24" height="6" fill="#3A2416"/><rect x="-12" y="50" width="24" height="6" fill="#3A2416"/></g>')
    gx, gy = 780, 1080
    s.append(f'<ellipse cx="{gx}" cy="{gy + 6}" rx="80" ry="10" fill="#2B1E10" opacity="0.3"/><rect x="{gx - 70}" y="{gy - 210}" width="12" height="212" fill="#4A2E1A"/><rect x="{gx + 58}" y="{gy - 210}" width="12" height="212" fill="#4A2E1A"/><rect x="{gx - 80}" y="{gy - 222}" width="160" height="16" fill="#3A2416"/>')
    s.append(f'<path d="M{gx - 20} {gy - 206} L{gx - 20} {gy - 178} M{gx + 20} {gy - 206} L{gx + 20} {gy - 178}" stroke="#3A2416" stroke-width="2"/><circle cx="{gx}" cy="{gy - 120}" r="56" fill="url(#bronze)"/><circle cx="{gx}" cy="{gy - 120}" r="40" fill="none" stroke="#7E5622" stroke-width="3"/><circle cx="{gx}" cy="{gy - 120}" r="14" fill="#E9C47A"/>')
    s.append(f'<path d="M{gx - 100} {gy} L{gx - 60} {gy - 80}" stroke="#6E4428" stroke-width="7" stroke-linecap="round"/><circle cx="{gx - 58}" cy="{gy - 84}" r="10" fill="#D9BC7C"/>')
    for cx, cy, r in ((260, 1060, 1), (380, 980, 0.8)):
        s.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{60 * r}" ry="{16 * r}" fill="#1E2C4A"/><ellipse cx="{cx}" cy="{cy - 4 * r}" rx="{54 * r}" ry="{12 * r}" fill="#2B3C60"/>')
    s.append(f'<g id="d-night" display="none"><rect width="{W}" height="{H}" fill="#0D1636" opacity="0.45"/>' + ''.join(f'<circle cx="{lx}" cy="{ly}" r="{r}" fill="url(#glow)"/>' for lx, ly, r in ((300, 172, 90), (600, 172, 90), (450, 266, 60), (450, 586, 40))) + '</g>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" class="scene dojo" role="img" aria-label="Inside your dojo">{defs()}{"".join(s)}</svg>'

if __name__ == '__main__':
    out = sys.argv[1]
    open(f'{out}/dojo.svg', 'w').write(scene())
