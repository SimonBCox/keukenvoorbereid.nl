"""Logo van Keukenvoorbereid, op dezelfde manier gebouwd als dat van De Draagmuurkoning.

Zelfde opbouw als website/draagmuurkoning.nl/images/logo/bouw_logo.py: letters als
omtrekken uit Poppins SemiBold, het tweede woord in goud, een gouden teken boven de
woord en een onderregel in Poppins Medium met gouden lijntjes ernaast. Waar de kroon
boven de laatste letter staat, is de druppel hier de punt op de i (25-10, variant C
uit het keuzeblad; tot die dag stond hij boven de d, naast de gewone i-punt).
"""

import sys
from pathlib import Path

import fitz
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

FONTS = Path(sys.argv[1])
DOEL = Path(sys.argv[2])
DOEL.mkdir(parents=True, exist_ok=True)

WOORD_DONKER = "Keuken"
# Met een puntloze i (U+0131): de druppel neemt de plaats van de punt in.
WOORD_GOUD = "voorbereıd"
ONDERREGEL = "SPECIALIST IN KEUKENVERBOUWING"

CAP = 100.0
MARGE = 14.0
REGEL_BREEDTE = 0.60
REGEL_SPATIE = 0.24

KLEUREN = {
    "donker": ("#202020", "#B68227"),
    "licht": ("#EFECE5", "#E2A43C"),
    "licht_roze": ("#EFECE5", "#E8508A"),
    # Op wit een dieper roze, zoals het goud daar ook donkerder is (contrast 4,3:1).
    "donker_roze": ("#202020", "#D4417C"),
    # Paars als alternatief voor roze (22-10): zelfde contrast op coal, dieper op wit.
    "licht_paars": ("#EFECE5", "#9B6BF2"),
    "donker_paars": ("#202020", "#7A45D1"),
}


class Zetter:
    def __init__(self, bestand):
        self.font = TTFont(bestand)
        self.glyfs = self.font.getGlyphSet()
        self.cmap = self.font.getBestCmap()
        self.upem = self.font["head"].unitsPerEm
        self.hmtx = self.font["hmtx"]
        os2 = self.font["OS/2"]
        self.cap = os2.sCapHeight
        self.xh = os2.sxHeight
        self.desc = abs(self.font["hhea"].descent)

    def grenzen(self, teken):
        g = self.font["glyf"][self.cmap[ord(teken)]]
        return g.xMin, g.xMax, g.yMax

    def punt_onder(self, teken="i"):
        """Onderkant van de hoogste contour van een teken, voor de i de punt."""
        tabel = self.font["glyf"]
        coords, eind, _ = tabel[self.cmap[ord(teken)]].getCoordinates(tabel)
        contouren, begin = [], 0
        for e in eind:
            contouren.append(coords[begin:e + 1])
            begin = e + 1
        return max(min(y for _, y in c) for c in contouren)

    def zet(self, tekst, spatie_em=0.0):
        paden, x, posities = [], 0.0, []
        for teken in tekst:
            naam = self.cmap.get(ord(teken))
            if naam is None:
                x += self.upem * 0.28
                posities.append(x)
                continue
            posities.append(x)
            pen = SVGPathPen(self.glyfs)
            self.glyfs[naam].draw(pen)
            d = pen.getCommands()
            if d:
                paden.append(f'<path transform="translate({x:.1f},0)" d="{d}"/>')
            x += self.hmtx[naam][0] + spatie_em * self.upem
        if spatie_em:
            x -= spatie_em * self.upem
        return "".join(paden), x, posities


def druppelpad(cx, onder, b, h):
    """Druppel met de punt naar boven: rond onderaan, spits bovenaan."""
    r = b / 2
    midden = onder - r
    top = onder - h
    k = 0.55 * r
    return (
        f"M {cx:.2f},{top:.2f} "
        f"C {cx + k * 0.35:.2f},{top + (h - r) * 0.45:.2f} {cx + r:.2f},{midden - r * 0.55:.2f} {cx + r:.2f},{midden:.2f} "
        f"A {r:.2f},{r:.2f} 0 0 1 {cx - r:.2f},{midden:.2f} "
        f"C {cx - r:.2f},{midden - r * 0.55:.2f} {cx - k * 0.35:.2f},{top + (h - r) * 0.45:.2f} {cx:.2f},{top:.2f} Z"
    )


def bouw(met_onderregel=True):
    woord = Zetter(FONTS / "Poppins-SemiBold.ttf")
    regel = Zetter(FONTS / "Poppins-Medium.ttf")

    S = CAP / woord.cap
    pad_donker, br_donker, _ = woord.zet(WOORD_DONKER)
    pad_goud, br_goud, pos_goud = woord.zet(WOORD_GOUD)
    breedte_woord = (br_donker + br_goud) * S
    staart = woord.desc * S

    # De druppel staat op de puntloze i, met zijn onderkant waar de i-punt begon,
    # en is even groot als toen hij boven de d stond. Hij steekt boven de stok van
    # de d uit; de ruimte boven het woord volgt uit wat het hoogst komt.
    i_xmin, i_xmax, _ = woord.grenzen("ı")
    _, _, d_ymax = woord.grenzen("d")
    stok = d_ymax * S
    druppel_onder = woord.punt_onder("i") * S
    druppel_b = CAP * 0.30
    druppel_h = CAP * 0.44
    boven = max(druppel_onder + druppel_h, stok) - CAP

    pad_regel, br_regel_font, _ = regel.zet(ONDERREGEL, REGEL_SPATIE)
    S_regel = (REGEL_BREEDTE * breedte_woord) / br_regel_font
    breedte_regel = br_regel_font * S_regel
    cap_regel = regel.cap * S_regel

    basislijn = MARGE + boven + CAP
    onder_woord = basislijn + staart
    if met_onderregel:
        regel_basislijn = onder_woord + CAP * 0.30 + cap_regel
        hoogte = regel_basislijn + MARGE
    else:
        hoogte = onder_woord + MARGE
    breedte = breedte_woord + 2 * MARGE
    x_woord = MARGE

    x_i = x_woord + (br_donker + pos_goud[-2]) * S
    cx = x_i + (i_xmin + i_xmax) / 2 * S
    druppel = druppelpad(cx, basislijn - druppel_onder, druppel_b, druppel_h)

    stam = "logo_kv" if met_onderregel else "logo_kv_wordmerk"
    for naam_kleur, (tekst_kleur, goud_kleur) in KLEUREN.items():
        delen = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {breedte:.1f} {hoogte:.1f}" width="{breedte:.0f}" height="{hoogte:.0f}" role="img" aria-label="Keukenvoorbereid">',
            "<title>Keukenvoorbereid</title>",
            f'<g fill="{tekst_kleur}" transform="translate({x_woord:.2f},{basislijn:.2f}) scale({S:.5f},-{S:.5f})">{pad_donker}</g>',
            f'<g fill="{goud_kleur}" transform="translate({x_woord + br_donker * S:.2f},{basislijn:.2f}) scale({S:.5f},-{S:.5f})">{pad_goud}</g>',
            f'<path fill="{goud_kleur}" d="{druppel}"/>',
        ]
        if met_onderregel:
            x_regel = (breedte - breedte_regel) / 2
            y_lijn = regel_basislijn - cap_regel / 2
            blok = 0.80 * breedte_woord
            lijn_lengte = max((blok - breedte_regel) / 2 - CAP * 0.16, 6)
            x_lijn_links = (breedte - blok) / 2
            delen += [
                f'<g fill="{tekst_kleur}" transform="translate({x_regel:.2f},{regel_basislijn:.2f}) scale({S_regel:.5f},-{S_regel:.5f})">{pad_regel}</g>',
                f'<rect fill="{goud_kleur}" x="{x_lijn_links:.2f}" y="{y_lijn:.2f}" width="{lijn_lengte:.2f}" height="{CAP*0.022:.2f}"/>',
                f'<rect fill="{goud_kleur}" x="{breedte - x_lijn_links - lijn_lengte:.2f}" y="{y_lijn:.2f}" width="{lijn_lengte:.2f}" height="{CAP*0.022:.2f}"/>',
            ]
        delen.append("</svg>")
        svg = DOEL / f"{stam}_{naam_kleur}.svg"
        svg.write_text("\n".join(delen), encoding="utf-8")
        pix = fitz.open(svg)[0].get_pixmap(alpha=False, dpi=110)
        pix.save(svg.with_suffix(".png"))
    print(f"{stam:18} {breedte:6.0f} x {hoogte:5.0f}  stok {stok:.0f}")


bouw(True)
bouw(False)
