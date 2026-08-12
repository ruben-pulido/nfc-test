"""
Generic treble-staff SVG renderer supporting arbitrary letter/octave/
accidental note sequences (extends the earlier interval-only renderer to
also handle sharps/flats, needed for the MLT pattern set).
"""
import sys
sys.path.insert(0, '.')
from solfege import diatonic_step

gclef_path = open("gclef_path.txt").read()

LINE_GAP = 18
STAFF_LEFT = 90
NOTE_SPACING = 90
NOTE_START_X = 210
STEP = LINE_GAP / 2

ACCENT = '#4f7cff'


def ledger_positions(step, staff_bottom_y):
    lines = []
    if step < 0:
        s = -2
        while s >= step:
            if s % 2 == 0:
                lines.append(staff_bottom_y - s * STEP)
            s -= 1
    elif step > 8:
        s = 10
        while s <= step:
            if s % 2 == 0:
                lines.append(staff_bottom_y - s * STEP)
            s += 1
    return lines


def render_staff_svg(notes, out_path, accent_color=ACCENT):
    """notes: list of {letter, accidental, octave} dicts (as from solfege.resolve_pitches)"""
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

    clef_scale = 0.088
    clef_x = STAFF_LEFT + 6
    svg.append(f'<path d="{gclef_path}" fill="#e8e8ef" transform="translate({clef_x},{staff_bottom_y}) scale({clef_scale},{-clef_scale})"/>')

    x = NOTE_START_X
    for note in notes:
        step = diatonic_step(note['letter'], note['octave'])
        cy = staff_bottom_y - step * STEP

        for ly in ledger_positions(step, staff_bottom_y):
            svg.append(f'<line x1="{x-16}" y1="{ly}" x2="{x+16}" y2="{ly}" stroke="#e8e8ef" stroke-width="2"/>')

        stem_up = step < 4
        if stem_up:
            stem_x = x + 8.5
            svg.append(f'<line x1="{stem_x}" y1="{cy-2}" x2="{stem_x}" y2="{cy-60}" stroke="{accent_color}" stroke-width="2.5"/>')
        else:
            stem_x = x - 8.5
            svg.append(f'<line x1="{stem_x}" y1="{cy+2}" x2="{stem_x}" y2="{cy+60}" stroke="{accent_color}" stroke-width="2.5"/>')

        # accidental glyph, placed left of the notehead
        if note['accidental'] == '#':
            svg.append(f'<text x="{x-24}" y="{cy+7}" font-size="26" fill="{accent_color}" font-family="serif">&#9839;</text>')
        elif note['accidental'] == 'b':
            svg.append(f'<text x="{x-22}" y="{cy+8}" font-size="26" fill="{accent_color}" font-family="serif">&#9837;</text>')

        svg.append(f'<ellipse cx="{x}" cy="{cy}" rx="10" ry="7.5" fill="{accent_color}" transform="rotate(-18 {x} {cy})"/>')
        x += NOTE_SPACING

    svg.append('</svg>')
    with open(out_path, 'w') as f:
        f.write('\n'.join(svg))
