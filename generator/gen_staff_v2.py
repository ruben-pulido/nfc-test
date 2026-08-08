gclef_path = open("/home/claude/gclef_path.txt").read()

LINE_GAP = 18
STAFF_LEFT = 90
NOTE_SPACING = 90
NOTE_START_X = 210

STEP = LINE_GAP / 2
NOTE_ORDER = ['E4','F4','G4','A4','B4','C5','D5','E5','F5','G5']
NOTE_ORDER_BELOW = ['D4','C4','B3','A3','G3']

def step_of(note):
    if note in NOTE_ORDER:
        return NOTE_ORDER.index(note)
    if note in NOTE_ORDER_BELOW:
        return -(NOTE_ORDER_BELOW.index(note) + 1)
    raise ValueError(note)

def y_of(note, staff_bottom_y):
    return staff_bottom_y - step_of(note) * STEP

def ledger_positions(note, staff_bottom_y):
    s = step_of(note)
    lines = []
    if s < 0:
        step = -2
        while step >= s:
            if step % 2 == 0:
                lines.append(staff_bottom_y - step * STEP)
            step -= 1
    elif s > 8:
        step = 10
        while step <= s:
            if step % 2 == 0:
                lines.append(staff_bottom_y - step * STEP)
            step += 1
    return lines

def render_svg(notes, out_path, accent_color):
    staff_top_y = 50
    staff_bottom_y = staff_top_y + LINE_GAP * 4
    content_width = NOTE_START_X + NOTE_SPACING * len(notes) + 60
    content_height = 260

    TOP_MARGIN, BOTTOM_MARGIN = 25, 15
    vb_y = -TOP_MARGIN
    vb_h = content_height + TOP_MARGIN + BOTTOM_MARGIN

    svg = [f'<svg viewBox="0 {vb_y} {content_width} {vb_h}" xmlns="http://www.w3.org/2000/svg">']
    svg.append(f'<rect x="0" y="{vb_y}" width="{content_width}" height="{vb_h}" fill="#10131a"/>')

    for i in range(5):
        y = staff_top_y + i * LINE_GAP
        svg.append(f'<line x1="{STAFF_LEFT}" y1="{y}" x2="{content_width-40}" y2="{y}" stroke="#e8e8ef" stroke-width="2"/>')

    # Vector treble clef (self-contained glyph outline, no font dependency)
    clef_scale = 0.088
    clef_x = STAFF_LEFT + 6
    svg.append(f'<path d="{gclef_path}" fill="#e8e8ef" transform="translate({clef_x},{staff_bottom_y}) scale({clef_scale},{-clef_scale})"/>')

    x = NOTE_START_X
    for note in notes:
        cy = y_of(note, staff_bottom_y)
        for ly in ledger_positions(note, staff_bottom_y):
            svg.append(f'<line x1="{x-16}" y1="{ly}" x2="{x+16}" y2="{ly}" stroke="#e8e8ef" stroke-width="2"/>')
        s = step_of(note)
        stem_up = s < 4
        if stem_up:
            stem_x = x + 8.5
            svg.append(f'<line x1="{stem_x}" y1="{cy-2}" x2="{stem_x}" y2="{cy-60}" stroke="{accent_color}" stroke-width="2.5"/>')
        else:
            stem_x = x - 8.5
            svg.append(f'<line x1="{stem_x}" y1="{cy+2}" x2="{stem_x}" y2="{cy+60}" stroke="{accent_color}" stroke-width="2.5"/>')
        svg.append(f'<ellipse cx="{x}" cy="{cy}" rx="10" ry="7.5" fill="{accent_color}" transform="rotate(-18 {x} {cy})"/>')
        x += NOTE_SPACING

    svg.append('</svg>')
    with open(out_path, 'w') as f:
        f.write('\n'.join(svg))

ACCENT = '#4f7cff'  # single consistent color across all tags — no color hinting

INTERVALS = [
    (1, ['C4','C4']),
    (2, ['C4','D4']),
    (3, ['C4','E4']),
    (4, ['C4','F4']),
    (5, ['C4','G4']),
    (6, ['C4','A4']),
    (7, ['C4','B4']),
    (8, ['C4','C5']),
]

for n, notes in INTERVALS:
    render_svg(notes, f'/home/claude/nfc-site/images/tag{n}.svg', ACCENT)
    print(f'tag{n}.svg done ({notes})')
