from __future__ import annotations

from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont, JpegImagePlugin  # noqa: F401


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "linkedin_assets"
LOGO_PATHS = [
    Path(r"C:\Users\90541\Downloads\nexivo-linkedin-logo-kare.png"),
    Path(r"C:\Users\90541\Downloads\nexivo-logo.png"),
]

W, H = 2160, 2700
BG = "#071312"
PANEL = "#F6F5EE"
INK = "#071312"
MUTED = "#65706D"
TEAL = "#0B6B63"
GREEN = "#21C083"
GOLD = "#D9B15F"
BLUE = "#3A86FF"
CORAL = "#FF6B4A"

FONT_REG = r"C:\Windows\Fonts\arial.ttf"
FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size=size)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            lines.append("")
            continue
        words = paragraph.split()
        line = ""
        for word in words:
            test = f"{line} {word}".strip()
            if draw.textbbox((0, 0), test, font=fnt)[2] <= max_width:
                line = test
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    fnt: ImageFont.FreeTypeFont,
    fill: str,
    max_width: int,
    line_gap: int = 18,
) -> int:
    x, y = xy
    for line in wrap_text(draw, text, fnt, max_width):
        if not line:
            y += fnt.size + line_gap
            continue
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap
    return y


def load_logo(size: int = 220) -> Image.Image | None:
    for path in LOGO_PATHS:
        if path.exists():
            logo = Image.open(path).convert("RGBA")
            logo.thumbnail((size, size), Image.Resampling.LANCZOS)
            return logo
    return None


def base_card(title: str, kicker: str, index: str | None = None) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Background structure
    draw.rectangle((0, 0, W, 260), fill="#0D2421")
    draw.rectangle((0, H - 210, W, H), fill="#0D2421")
    for i in range(0, W, 180):
        draw.line((i, 300, i + 620, H - 260), fill="#102B28", width=3)
    for y in range(420, H - 320, 300):
        draw.line((140, y, W - 140, y), fill="#102B28", width=2)

    logo = load_logo(185)
    if logo:
        img.paste(logo, (120, 72), logo)
    else:
        draw.rounded_rectangle((120, 70, 300, 250), radius=28, fill="#061C19", outline=GREEN, width=4)
        draw.text((157, 116), "NX", font=font(58, True), fill=PANEL)

    draw.text((330, 83), "NEXIVO", font=font(64, True), fill=PANEL)
    draw.text((333, 162), "Codex-powered technical log", font=font(34), fill="#A9C5BE")

    if index:
        draw.rounded_rectangle((W - 310, 92, W - 120, 178), radius=42, fill=GREEN)
        draw.text((W - 255, 112), index, font=font(42, True), fill=BG)

    draw.text((150, 370), kicker.upper(), font=font(38, True), fill=GREEN)
    draw_wrapped(draw, (150, 470), title, font(116, True), PANEL, W - 300, 26)
    return img, draw


def footer(draw: ImageDraw.ImageDraw, note: str = "AI workers, not human employees. Work tracked on GitHub.") -> None:
    draw.text((150, H - 145), note, font=font(34), fill="#A9C5BE")


def bullet_list(draw: ImageDraw.ImageDraw, items: list[str], x: int, y: int, max_width: int, color: str = PANEL) -> int:
    for item in items:
        draw.ellipse((x, y + 16, x + 22, y + 38), fill=GREEN)
        y = draw_wrapped(draw, (x + 48, y), item, font(54, True), color, max_width - 48, 14) + 26
    return y


def save(img: Image.Image, name: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    img.save(path, quality=95, optimize=True)
    return path


def draw_agent_grid(draw: ImageDraw.ImageDraw, agents: list[tuple[str, str]], x: int, y: int, cols: int = 2) -> None:
    card_w = 850
    card_h = 250
    gap_x = 70
    gap_y = 60
    colors = [GREEN, GOLD, BLUE, CORAL, "#8BE0D4", "#C6A3FF"]
    for idx, (name, role) in enumerate(agents):
        col = idx % cols
        row = idx // cols
        x0 = x + col * (card_w + gap_x)
        y0 = y + row * (card_h + gap_y)
        accent = colors[idx % len(colors)]
        draw.rounded_rectangle((x0, y0, x0 + card_w, y0 + card_h), radius=34, fill="#0D2421", outline="#21443F", width=4)
        draw.rectangle((x0, y0, x0 + 18, y0 + card_h), fill=accent)
        draw.text((x0 + 60, y0 + 50), name, font=font(58, True), fill=PANEL)
        draw.text((x0 + 60, y0 + 132), role, font=font(37), fill="#A9C5BE")


AGENTS = [
    ("Hypatia", "AI CTO"),
    ("Kierkegaard", "Computer Vision"),
    ("Averroes", "Hardware Strategy"),
    ("Dalton", "Biometrics Testing"),
    ("Aquinas", "Open Dataset Research"),
    ("Boyle", "Score Review"),
]


def carousel() -> list[Path]:
    paths: list[Path] = []

    img, draw = base_card("Before hardware, I built an AI technical team.", "NEXIVO x Codex", "01/08")
    draw_wrapped(draw, (150, 980), "A founder-led deep-tech experiment: turn Codex workers into a trackable pre-MVP technical rhythm.", font(58), "#CDE7DF", W - 300, 18)
    footer(draw)
    paths.append(save(img, "carousel_01_launch.png"))

    img, draw = base_card("These are not human employees.", "Transparency first", "02/08")
    bullet_list(draw, ["Codex worker codenames", "AI agents with scoped tasks", "No fake personal profiles", "Every output tracked in GitHub"], 170, 1010, W - 340)
    footer(draw, "We use AI workers as a work system, not as fake people.")
    paths.append(save(img, "carousel_02_transparency.png"))

    img, draw = base_card("Meet the Codex workers.", "The team map", "03/08")
    draw_agent_grid(draw, AGENTS, 150, 930)
    footer(draw)
    paths.append(save(img, "carousel_03_team.png"))

    img, draw = base_card("Each worker owns a thinking lane.", "Role design", "04/08")
    lanes = [
        "Hypatia reviews strategy and architecture.",
        "Kierkegaard questions what images reveal.",
        "Averroes turns hardware choices into evidence.",
        "Dalton measures biometric scores and thresholds.",
        "Aquinas tests sources, datasets and method.",
        "Boyle asks whether the result was actually measured.",
    ]
    bullet_list(draw, lanes, 170, 900, W - 340, "#EAF6F2")
    footer(draw)
    paths.append(save(img, "carousel_04_lanes.png"))

    img, draw = base_card("What they shipped before hardware.", "Pre-hardware output", "05/08")
    shipped = [
        "Python + OpenCV vein biometrics pipeline",
        "Synthetic smoke test",
        "Open finger-vein dataset validation",
        "FAR / FRR and threshold analysis",
        "Hardware shopping list and setup plan",
        "First real test protocol",
    ]
    bullet_list(draw, shipped, 170, 900, W - 340)
    footer(draw)
    paths.append(save(img, "carousel_05_shipped.png"))

    img, draw = base_card("The proof is not a pitch deck.", "Public log", "06/08")
    draw.rounded_rectangle((170, 940, W - 170, 1880), radius=48, fill=PANEL)
    inner = ImageDraw.Draw(img)
    inner.text((250, 1030), "Issues", font=font(72, True), fill=TEAL)
    inner.text((250, 1180), "Commits", font=font(72, True), fill=TEAL)
    inner.text((250, 1330), "Docs", font=font(72, True), fill=TEAL)
    inner.text((250, 1480), "Tests", font=font(72, True), fill=TEAL)
    inner.text((250, 1630), "Reviews", font=font(72, True), fill=TEAL)
    draw_wrapped(draw, (850, 1060), "Every task has a record. Every claim points back to work.", font(72, True), INK, 980, 20)
    footer(draw, "GitHub link goes in the pinned comment.")
    paths.append(save(img, "carousel_06_proof.png"))

    img, draw = base_card("This is not product validation yet.", "Still early", "07/08")
    nexts = [
        "Real NIR hardware",
        "First vein image",
        "Image quality metrics",
        "FAR / FRR on our own samples",
        "Liveness / PAD planning",
        "KVKK / GDPR security review",
    ]
    bullet_list(draw, nexts, 170, 930, W - 340)
    footer(draw, "Pre-hardware sanity check, not a market-ready biometric product.")
    paths.append(save(img, "carousel_07_next.png"))

    img, draw = base_card("Maybe this is how early teams start.", "Founder lesson", "08/08")
    draw_wrapped(draw, (160, 920), "Few humans.\nWell-scoped AI workers.\nTransparent logs.\nFast iteration.", font(102, True), PANEL, W - 320, 26)
    draw_wrapped(draw, (160, 1680), "Next: capture the first vein image with real NIR hardware.", font(60), "#CDE7DF", W - 320, 20)
    footer(draw, "NEXIVO technical log in the pinned comment.")
    paths.append(save(img, "carousel_08_lesson.png"))

    # PDF carousel
    pdf_path = OUT / "nexivo_ai_team_launch_carousel.pdf"
    rgb_images = [Image.open(path).convert("RGB") for path in paths]
    rgb_images[0].save(pdf_path, save_all=True, append_images=rgb_images[1:], resolution=144.0)
    paths.append(pdf_path)
    return paths


def post2_visual() -> Path:
    img, draw = base_card("If they lived today, what would they build?", "Codename story", None)
    summaries = [
        ("Hypatia", "AI CTO: ethical systems architecture"),
        ("Kierkegaard", "CV: what does an image reveal?"),
        ("Averroes", "Hardware: evidence-led choices"),
        ("Dalton", "Biometrics: thresholds and measurement"),
        ("Aquinas", "Datasets: sources and method"),
        ("Boyle", "Review: was it actually measured?"),
    ]
    draw_agent_grid(draw, summaries, 150, 900)
    footer(draw, "Codex worker codenames, not human employees.")
    return save(img, "post_02_codename_story.png")


def post3_visual() -> Path:
    img, draw = base_card("What we completed before buying hardware.", "Pre-hardware proof", None)
    items = [
        "OpenCV pipeline",
        "Synthetic smoke test",
        "Open dataset validation",
        "Same/different score analysis",
        "Threshold and FAR / FRR review",
        "Hardware list",
        "First test protocol",
        "KVKK / consent draft",
        "Competitive analysis",
        "GitHub issue + commit log",
    ]
    y = 860
    for i, item in enumerate(items, 1):
        x = 170 if i <= 5 else 1110
        yy = y + ((i - 1) % 5) * 265
        draw.rounded_rectangle((x, yy, x + 840, yy + 190), radius=34, fill="#0D2421", outline="#21443F", width=4)
        draw.text((x + 42, yy + 42), f"{i:02d}", font=font(48, True), fill=GREEN)
        draw_wrapped(draw, (x + 150, yy + 38), item, font(44, True), PANEL, 620, 10)
    footer(draw, "The first step was not hardware. It was knowing what to measure.")
    return save(img, "post_03_pre_hardware_proof.png")


def post4_visual() -> Path:
    img, draw = base_card("AI did not give me a team. It taught me how to lead one.", "Founder lesson", None)
    steps = [
        ("Founder", "clear intent"),
        ("Codex workers", "scoped roles"),
        ("Issues", "tasks"),
        ("Commits", "work"),
        ("Docs", "memory"),
        ("MVP readiness", "next test"),
    ]
    x0, y0 = 170, 980
    for idx, (label, sub) in enumerate(steps):
        x = x0 + (idx % 2) * 930
        y = y0 + (idx // 2) * 390
        draw.rounded_rectangle((x, y, x + 780, y + 245), radius=44, fill=PANEL)
        draw.text((x + 50, y + 48), label, font=font(58, True), fill=INK)
        draw.text((x + 50, y + 136), sub, font=font(40), fill=TEAL)
        if idx < len(steps) - 1:
            draw.line((x + 780, y + 122, x + 900, y + 122), fill=GREEN, width=8)
    footer(draw, "AI is not the team. AI is the system you learn to manage.")
    return save(img, "post_04_founder_lesson.png")


def main() -> None:
    generated = []
    generated.extend(carousel())
    generated.append(post2_visual())
    generated.append(post3_visual())
    generated.append(post4_visual())

    for path in generated:
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
