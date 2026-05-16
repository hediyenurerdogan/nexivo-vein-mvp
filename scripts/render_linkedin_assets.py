from __future__ import annotations

from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont, JpegImagePlugin  # noqa: F401


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "linkedin_assets"
LOGO_PATHS = [
    ROOT / "docs" / "linkedin_assets" / "nexivo-linkedin-logo.png",
    Path(r"C:\Users\90541\Downloads\nexivo-linkedin-assets\nexivo-linkedin-logo.png"),
    Path(r"C:\Users\90541\Downloads\nexivo-linkedin-logo-kare.png"),
    Path(r"C:\Users\90541\Downloads\nexivo-logo.png"),
]

W, H = 2160, 2700
BG = "#F4F8F6"
PANEL = "#FFFFFF"
INK = "#071312"
MUTED = "#667672"
TEAL = "#0B6B63"
GREEN = "#19B99A"
GOLD = "#D9B15F"
BLUE = "#3A86FF"
CORAL = "#FF6B4A"

FONT_REG = r"C:\Windows\Fonts\arial.ttf"
FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size=size)


def tr_upper(text: str) -> str:
    return text.replace("i", "İ").replace("ı", "I").upper()


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

    # Light technical canvas: enough structure for NEXIVO, without the heavy black-poster look.
    draw.rectangle((0, 0, W, 300), fill="#EAF3F0")
    draw.rectangle((0, H - 170, W, H), fill="#EAF3F0")
    for i in range(-120, W, 230):
        draw.line((i, 330, i + 520, H - 250), fill="#D7E7E3", width=3)
    for y in range(455, H - 300, 320):
        draw.line((140, y, W - 140, y), fill="#DCEBE7", width=2)

    logo = load_logo(210)
    if logo:
        x_logo, y_logo = 120, 45
        draw.rounded_rectangle((x_logo - 18, y_logo - 18, x_logo + 228, y_logo + 228), radius=36, fill="#071312")
        img.paste(logo, (x_logo, y_logo), logo)
    else:
        draw.rounded_rectangle((120, 45, 330, 255), radius=36, fill="#071312")
        draw.text((178, 100), "N", font=font(92, True), fill=PANEL)

    draw.text((390, 80), "NEXIVO", font=font(66, True), fill=INK)
    draw.text((393, 162), "Multi-agent destekli teknik kayıt", font=font(34), fill=MUTED)

    if index:
        draw.rounded_rectangle((W - 315, 92, W - 120, 178), radius=42, fill=INK)
        draw.text((W - 262, 112), index, font=font(42, True), fill=PANEL)

    draw.text((150, 390), tr_upper(kicker), font=font(38, True), fill=TEAL)
    draw_wrapped(draw, (150, 500), title, font(112, True), INK, W - 300, 26)
    return img, draw


def footer(draw: ImageDraw.ImageDraw, note: str | None = None) -> None:
    if note:
        draw.text((150, H - 112), note, font=font(34), fill=MUTED)
    draw.text((W - 370, H - 112), "nexivo-vein-mvp", font=font(34, True), fill=TEAL)


def bullet_list(draw: ImageDraw.ImageDraw, items: list[str], x: int, y: int, max_width: int, color: str = INK) -> int:
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
        draw.rounded_rectangle((x0, y0, x0 + card_w, y0 + card_h), radius=34, fill=PANEL, outline="#CFE2DD", width=4)
        draw.rectangle((x0, y0, x0 + 18, y0 + card_h), fill=accent)
        draw.text((x0 + 60, y0 + 50), name, font=font(58, True), fill=INK)
        draw.text((x0 + 60, y0 + 132), role, font=font(37), fill=MUTED)


AGENTS = [
    ("Hypatia", "CTO Agent"),
    ("Kierkegaard", "Computer Vision"),
    ("Averroes", "Donanım Stratejisi"),
    ("Dalton", "Biyometrik Test"),
    ("Aquinas", "Açık Veri Araştırması"),
    ("Boyle", "Skor İncelemesi"),
]


def carousel() -> list[Path]:
    paths: list[Path] = []

    img, draw = base_card("Donanım almadan önce yapay zeka tabanlı bir teknik ekip kurdum.", "NEXIVO x MULTI-AGENT", "01/08")
    draw_wrapped(draw, (150, 1040), "Otonom AI Agent'larla izlenebilir bir pre-MVP teknik çalışma ritmi kurma deneyi.", font(58), MUTED, W - 300, 18)
    footer(draw)
    paths.append(save(img, "carousel_01_launch.png"))

    img, draw = base_card("Bu ekip, gerçek kişilerden değil tanımlı AI rollerinden oluşuyor.", "Önce şeffaflık", "02/08")
    bullet_list(draw, ["Agent kod adları", "Net görevli AI Agent'lar", "Sahte kişisel profil yok", "Her çıktı GitHub'da kayıtlı"], 170, 1110, W - 340)
    footer(draw, "Şeffaflık için: bunlar insan profili değil, çalışma rolleri.")
    paths.append(save(img, "carousel_02_transparency.png"))

    img, draw = base_card("AI Agent ekibiyle tanışın.", "Ekip haritası", "03/08")
    draw_agent_grid(draw, AGENTS, 150, 930)
    footer(draw)
    paths.append(save(img, "carousel_03_team.png"))

    img, draw = base_card("Her agent farklı bir düşünme hattı taşıyor.", "Rol tasarımı", "04/08")
    lanes = [
        "Hypatia strateji ve mimariyi gözden geçirir.",
        "Kierkegaard görüntünün ne anlattığını sorgular.",
        "Averroes donanım kararlarını kanıta bağlar.",
        "Dalton biyometrik skor ve eşikleri ölçer.",
        "Aquinas kaynak, veri seti ve yöntemi inceler.",
        "Boyle sonucun gerçekten ölçülüp ölçülmediğini sorar.",
    ]
    bullet_list(draw, lanes, 170, 900, W - 340, INK)
    footer(draw)
    paths.append(save(img, "carousel_04_lanes.png"))

    img, draw = base_card("Donanım gelmeden önce ne çıktı?", "Donanım öncesi çıktı", "05/08")
    shipped = [
        "Python + OpenCV damar biyometrisi pipeline'ı",
        "Sentetik smoke test",
        "Açık finger-vein veri seti doğrulaması",
        "FAR / FRR ve threshold analizi",
        "Donanım alışveriş listesi ve kurulum planı",
        "İlk gerçek test protokolü",
    ]
    bullet_list(draw, shipped, 170, 900, W - 340)
    footer(draw)
    paths.append(save(img, "carousel_05_shipped.png"))

    img, draw = base_card("Kanıt sunum dosyasında değil, GitHub kaydında.", "PUBLIC LOG", "06/08")
    flow_items = ["Issue", "Commit", "Doküman", "Test", "Review"]
    box_w = 285
    box_h = 180
    gap = 85
    start_x = 170
    y = 1040
    for idx, label in enumerate(flow_items):
        x = start_x + idx * (box_w + gap)
        draw.rounded_rectangle((x, y, x + box_w, y + box_h), radius=34, fill=PANEL, outline="#CFE2DD", width=3)
        label_width = draw.textbbox((0, 0), label, font=font(45, True))[2]
        draw.text((x + (box_w - label_width) // 2, y + 62), label, font=font(45, True), fill=TEAL)
    for idx in range(len(flow_items) - 1):
        x = start_x + idx * (box_w + gap)
        next_x = start_x + (idx + 1) * (box_w + gap)
        ax0 = x + box_w + 18
        ax1 = next_x - 24
        ay = y + box_h // 2
        draw.line((ax0, ay, ax1, ay), fill=GREEN, width=8)
        draw.polygon([(ax1, ay), (ax1 - 24, ay - 18), (ax1 - 24, ay + 18)], fill=GREEN)
    draw_wrapped(
        draw,
        (170, 1380),
        "Her iddia, şeffaf ve izlenebilir bir geliştirme sürecine bağlanıyor.",
        font(78, True),
        INK,
        W - 340,
        24,
    )
    footer(draw, "Tüm teknik kayıtlar ve GitHub linki sabit yorumda.")
    paths.append(save(img, "carousel_06_proof.png"))

    img, draw = base_card("Sıradaki iş: fikri gerçek donanımla sınamak.", "Sıradaki doğrulama", "07/08")
    nexts = [
        "NIR kamera ve ışıkla ilk gerçek damar görüntüsünü almak",
        "Görüntü kalitesini ölçmek",
        "Kendi örneklerimizde FAR / FRR skorlarını görmek",
        "Liveness / PAD risklerini planlamak",
        "KVKK / GDPR güvenlik akışını netleştirmek",
    ]
    bullet_list(draw, nexts, 170, 1030, W - 340)
    footer(draw, "Bu sayfa, donanım gelince neyi test edeceğimizi gösterir.")
    paths.append(save(img, "carousel_07_next.png"))

    img, draw = base_card("Belki erken ekipler böyle başlayacak.", "Kurucu yorumu", "08/08")
    draw_wrapped(draw, (160, 920), "Az insan.\nİyi tanımlanmış AI Agent'lar.\nŞeffaf kayıt.\nHızlı iterasyon.", font(102, True), INK, W - 320, 26)
    draw_wrapped(draw, (160, 1680), "Sıradaki adım: gerçek NIR donanımıyla ilk damar görüntüsü.", font(60), MUTED, W - 320, 20)
    footer(draw, "NEXIVO teknik kaydı sabit yorumda.")
    paths.append(save(img, "carousel_08_lesson.png"))

    # PDF carousel
    pdf_path = OUT / "nexivo_ai_team_launch_carousel.pdf"
    rgb_images = [Image.open(path).convert("RGB") for path in paths]
    rgb_images[0].save(pdf_path, save_all=True, append_images=rgb_images[1:], resolution=144.0)
    paths.append(pdf_path)
    return paths


def post2_visual() -> Path:
    img, draw = base_card("Bugün yaşasalardı ne inşa ederlerdi?", "Codename hikayesi", None)
    summaries = [
        ("Hypatia", "CTO Agent: etik sistem mimarisi"),
        ("Kierkegaard", "CV: görüntü ne anlatıyor?"),
        ("Averroes", "Donanım: kanıta dayalı seçim"),
        ("Dalton", "Biyometri: eşik ve ölçüm"),
        ("Aquinas", "Veri: kaynak ve yöntem"),
        ("Boyle", "Review: gerçekten ölçüldü mü?"),
    ]
    draw_agent_grid(draw, summaries, 150, 900)
    footer(draw, "Agent kod adları; insan çalışan profili değil.")
    return save(img, "post_02_codename_story.png")


def post3_visual() -> Path:
    img, draw = base_card("Donanım almadan önce ne tamamladık?", "Donanım öncesi kanıt", None)
    items = [
        "OpenCV pipeline",
        "Sentetik smoke test",
        "Açık veri doğrulaması",
        "Aynı/farklı kişi skor analizi",
        "Threshold ve FAR / FRR review",
        "Donanım listesi",
        "İlk test protokolü",
        "KVKK / onam taslağı",
        "Rakip analizi",
        "GitHub issue + commit kaydı",
    ]
    y = 860
    for i, item in enumerate(items, 1):
        x = 170 if i <= 5 else 1110
        yy = y + ((i - 1) % 5) * 265
        draw.rounded_rectangle((x, yy, x + 840, yy + 190), radius=34, fill=PANEL, outline="#CFE2DD", width=4)
        draw.text((x + 42, yy + 42), f"{i:02d}", font=font(48, True), fill=GREEN)
        draw_wrapped(draw, (x + 150, yy + 38), item, font(44, True), INK, 620, 10)
    footer(draw, "İlk adım donanım değil; neyi ölçeceğini bilen sistemi kurmaktı.")
    return save(img, "post_03_pre_hardware_proof.png")


def post4_visual() -> Path:
    img, draw = base_card("Yapay zeka bana ekip vermedi. Ekip yönetmeyi öğretti.", "Kurucu dersi", None)
    steps = [
        ("Kurucu", "net niyet"),
        ("AI Agent", "tanımlı rol"),
        ("Issue", "görev"),
        ("Commit", "iş"),
        ("Doküman", "hafıza"),
        ("MVP hazırlığı", "sıradaki test"),
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
    footer(draw, "AI ekip değil; yönetmeyi öğrendiğin çalışma sistemi.")
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
