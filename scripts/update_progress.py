from datetime import date
from pathlib import Path
import xml.etree.ElementTree as ET
import html


# --------------------------------------------------
# Configuration
# --------------------------------------------------

SCHOOL_YEAR_START_MONTH = 9
SCHOOL_YEAR_START_DAY = 1

LOGO_PATH = Path("assets/epitech.svg")
OUTPUT_PATH = Path("assets/studies-progress.svg")

SVG_WIDTH = 700
SVG_HEIGHT = 180

LOGO_WIDTH = 220
LOGO_HEIGHT = 75

BAR_X = 70
BAR_Y = 105
BAR_WIDTH = 560
BAR_HEIGHT = 22


# --------------------------------------------------
# School year calculation
# --------------------------------------------------

today = date.today()

# September -> December:
# current school year = current_year / current_year + 1
#
# January -> August:
# current school year = current_year - 1 / current_year
if today.month >= SCHOOL_YEAR_START_MONTH:
    school_year_start = today.year
else:
    school_year_start = today.year - 1

school_year_end = school_year_start + 1

start_date = date(
    school_year_start,
    SCHOOL_YEAR_START_MONTH,
    SCHOOL_YEAR_START_DAY,
)

end_date = date(
    school_year_end,
    SCHOOL_YEAR_START_MONTH,
    SCHOOL_YEAR_START_DAY,
)

total_days = (end_date - start_date).days
elapsed_days = (today - start_date).days

progress = max(0.0, min(1.0, elapsed_days / total_days))
percentage = progress * 100

school_year_label = f"{school_year_start} — {school_year_end}"


# --------------------------------------------------
# Load Epitech logo and extract its contents
# --------------------------------------------------

if not LOGO_PATH.exists():
    raise FileNotFoundError(f"Logo not found: {LOGO_PATH}")

tree = ET.parse(LOGO_PATH)
root = tree.getroot()

viewbox = root.get("viewBox")

if not viewbox:
    width = root.get("width")
    height = root.get("height")

    if not width or not height:
        raise ValueError(
            "The Epitech SVG must contain either a viewBox "
            "or width/height attributes."
        )

    viewbox = f"0 0 {width} {height}"

logo_children = "\n".join(
    ET.tostring(child, encoding="unicode")
    for child in root
)


# --------------------------------------------------
# Progress bar
# --------------------------------------------------

progress_width = BAR_WIDTH * progress

# Avoid creating a bar with width 0 that can sometimes
# behave oddly in SVG renderers.
if progress_width < 1:
    progress_width = 0


# --------------------------------------------------
# Generate SVG
# --------------------------------------------------

svg = f'''<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{SVG_WIDTH}"
    height="{SVG_HEIGHT}"
    viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}">

    <!-- Epitech logo -->
    <svg
        x="{(SVG_WIDTH - LOGO_WIDTH) / 2}"
        y="5"
        width="{LOGO_WIDTH}"
        height="{LOGO_HEIGHT}"
        viewBox="{html.escape(viewbox, quote=True)}"
        preserveAspectRatio="xMidYMid meet">
        {logo_children}
    </svg>

    <!-- Progress bar -->
    <rect
        x="{BAR_X}"
        y="{BAR_Y}"
        width="{BAR_WIDTH}"
        height="{BAR_HEIGHT}"
        rx="{BAR_HEIGHT / 2}"
        fill="#21262d"/>

    <rect
        x="{BAR_X}"
        y="{BAR_Y}"
        width="{progress_width:.2f}"
        height="{BAR_HEIGHT}"
        rx="{BAR_HEIGHT / 2}"
        fill="#58a6ff"/>

    <!-- Percentage -->
    <text
        x="{SVG_WIDTH / 2}"
        y="143"
        text-anchor="middle"
        font-family="Arial, Helvetica, sans-serif"
        font-size="16"
        font-weight="700"
        fill="#58a6ff">
        {percentage:.2f}%
    </text>

    <!-- School year -->
    <text
        x="{SVG_WIDTH / 2}"
        y="165"
        text-anchor="middle"
        font-family="Arial, Helvetica, sans-serif"
        font-size="13"
        fill="#8b949e">
        {school_year_label}
    </text>

</svg>
'''


# --------------------------------------------------
# Write file
# --------------------------------------------------

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.write_text(svg, encoding="utf-8")

print(
    f"School year: {school_year_label} | "
    f"Date: {today} | "
    f"Progress: {percentage:.2f}%"
)
