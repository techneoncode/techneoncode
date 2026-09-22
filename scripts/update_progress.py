from datetime import date

START_DATE = date(2026, 9, 1)
END_DATE = date(2031, 7, 31)

today = date.today()

total_days = (END_DATE - START_DATE).days
elapsed_days = (today - START_DATE).days

progress = max(0, min(1, elapsed_days / total_days))
percentage = progress * 100

width, height = 700, 150

bar_x = 40
bar_y = 82
bar_w = 620
bar_h = 24

progress_w = max(0, bar_w * progress)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
    width="{width}"
    height="{height}"
    viewBox="0 0 {width} {height}">

  <rect
    width="{width}"
    height="{height}"
    rx="16"
    fill="#0d1117"/>

  <text
    x="40"
    y="38"
    font-family="Arial, sans-serif"
    font-size="20"
    font-weight="700"
    fill="#f0f6fc">
    🎓 Engineering Degree Progress
  </text>

  <text
    x="40"
    y="62"
    font-family="Arial, sans-serif"
    font-size="13"
    fill="#8b949e">
    EPITECH · Promotion 2031
  </text>

  <rect
    x="{bar_x}"
    y="{bar_y}"
    width="{bar_w}"
    height="{bar_h}"
    rx="12"
    fill="#21262d"/>

  <rect
    x="{bar_x}"
    y="{bar_y}"
    width="{progress_w:.2f}"
    height="{bar_h}"
    rx="12"
    fill="#58a6ff"/>

  <text
    x="{width - 40}"
    y="100"
    text-anchor="end"
    font-family="Arial, sans-serif"
    font-size="14"
    font-weight="700"
    fill="#f0f6fc">
    {percentage:.2f}%
  </text>

  <text
    x="40"
    y="130"
    font-family="Arial, sans-serif"
    font-size="12"
    fill="#8b949e">
    September 2026
  </text>

  <text
    x="{width - 40}"
    y="130"
    text-anchor="end"
    font-family="Arial, sans-serif"
    font-size="12"
    fill="#8b949e">
    July 2031
  </text>

</svg>'''

with open("assets/studies-progress.svg", "w", encoding="utf-8") as file:
    file.write(svg)

print(f"Progress: {percentage:.2f}%")
