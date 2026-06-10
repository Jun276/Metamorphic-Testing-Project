import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


SCRIPT_DIR = Path(__file__).resolve().parent
MNIST_PATH = SCRIPT_DIR / "metamorphic_testing" / "example" / "mnist"
OUTPUT_ROOT = SCRIPT_DIR / "ppt_slide_grids"

# None: create one slide image for every experiment folder.
# Example: "20260610192028" creates only that experiment.
TARGET_EXPERIMENT = None

CANVAS_WIDTH = 2400
CANVAS_HEIGHT = 1350
ROWS = 10
COLS = 21  # source #0 + follow-up #1~#20

PAD_X = 32
PAD_Y = 32
TITLE_HEIGHT = 88
COL_LABEL_HEIGHT = 44
ROW_LABEL_WIDTH = 86
CELL_GAP = 4
BORDER_WIDTH = 2

BACKGROUND = (248, 248, 246)
HEADER_BG = (232, 234, 236)
SOURCE_BG = (230, 241, 255)
CELL_BG = (255, 255, 255)
GRID_LINE = (175, 180, 188)
SOURCE_BORDER = (45, 105, 185)
OK_BORDER = (130, 135, 142)
FAIL_BORDER = (214, 68, 68)
TEXT = (25, 28, 32)
SUBTEXT = (80, 86, 94)


def get_font(size, bold=False):
    candidates = [
        Path("C:/Windows/Fonts/malgunbd.ttf" if bold else "C:/Windows/Fonts/malgun.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ]

    for font_path in candidates:
        if font_path.exists():
            return ImageFont.truetype(str(font_path), size)

    return ImageFont.load_default()


TITLE_FONT = get_font(30, bold=True)
LABEL_FONT = get_font(20, bold=True)
SMALL_FONT = get_font(16)


def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_centered_text(draw, rect, text, font, fill=TEXT):
    x1, y1, x2, y2 = rect
    width, height = text_size(draw, text, font)
    x = x1 + (x2 - x1 - width) / 2
    y = y1 + (y2 - y1 - height) / 2 - 1
    draw.text((x, y), text, font=font, fill=fill)


def image_index(path):
    match = re.match(r"#(\d+)_prediction_(\d+)\.png$", path.name)
    if not match:
        return None
    return int(match.group(1))


def prediction_value(path):
    match = re.match(r"#(\d+)_prediction_(\d+)\.png$", path.name)
    if not match:
        return None
    return int(match.group(2))


def id_number(path):
    match = re.match(r"ID_(\d+)$", path.name)
    if not match:
        return None
    return int(match.group(1))


def safe_filename(name):
    return re.sub(r'[<>:"/\\|?*]', "_", name)


def discover_experiments():
    experiments = []

    for path in MNIST_PATH.iterdir():
        if not path.is_dir():
            continue

        id_dirs = [p for p in path.iterdir() if p.is_dir() and id_number(p) is not None]
        if id_dirs:
            experiments.append(path)

    experiments.sort(key=lambda p: p.name)

    if TARGET_EXPERIMENT is not None:
        experiments = [p for p in experiments if p.name == TARGET_EXPERIMENT]

    return experiments


def collect_images(experiment_path):
    id_dirs = [p for p in experiment_path.iterdir() if p.is_dir() and id_number(p) is not None]
    id_dirs.sort(key=id_number)

    if len(id_dirs) < ROWS:
        print(f"Warning: {experiment_path.name} has only {len(id_dirs)} ID folders.")

    rows = []

    for id_dir in id_dirs[:ROWS]:
        image_map = {}

        for image_path in id_dir.glob("*.png"):
            index = image_index(image_path)
            if index is None:
                continue
            if 0 <= index <= 20:
                image_map[index] = image_path

        missing = [i for i in range(COLS) if i not in image_map]
        if missing:
            print(f"Warning: {experiment_path.name}/{id_dir.name} missing {missing}")

        rows.append((id_dir.name, image_map))

    return rows


def make_slide_grid(experiment_path):
    rows = collect_images(experiment_path)
    if not rows:
        print(f"Skipped: {experiment_path.name} has no images.")
        return None

    available_width = CANVAS_WIDTH - (PAD_X * 2) - ROW_LABEL_WIDTH - ((COLS - 1) * CELL_GAP)
    available_height = (
        CANVAS_HEIGHT
        - (PAD_Y * 2)
        - TITLE_HEIGHT
        - COL_LABEL_HEIGHT
        - ((ROWS - 1) * CELL_GAP)
    )
    cell_size = min(available_width // COLS, available_height // ROWS)

    grid_width = ROW_LABEL_WIDTH + (COLS * cell_size) + ((COLS - 1) * CELL_GAP)
    grid_height = COL_LABEL_HEIGHT + (ROWS * cell_size) + ((ROWS - 1) * CELL_GAP)
    start_x = (CANVAS_WIDTH - grid_width) // 2
    start_y = PAD_Y + TITLE_HEIGHT

    canvas = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(canvas)

    title = f"{experiment_path.name} | Source + Follow-up Inputs"
    subtitle = "Rows: ID_1~ID_10    Columns: Source #0, T1~T20    Red border: prediction changed"

    draw.text((PAD_X, PAD_Y), title, font=TITLE_FONT, fill=TEXT)
    draw.text((PAD_X, PAD_Y + 44), subtitle, font=SMALL_FONT, fill=SUBTEXT)

    draw.rounded_rectangle(
        [start_x, start_y, start_x + grid_width, start_y + grid_height],
        radius=8,
        fill=(242, 243, 244),
        outline=GRID_LINE,
        width=1,
    )

    # Column labels.
    for col in range(COLS):
        x = start_x + ROW_LABEL_WIDTH + col * (cell_size + CELL_GAP)
        y = start_y
        label = "Source" if col == 0 else f"T{col}"
        fill = SOURCE_BG if col == 0 else HEADER_BG
        draw.rectangle([x, y, x + cell_size, y + COL_LABEL_HEIGHT], fill=fill)
        draw_centered_text(draw, (x, y, x + cell_size, y + COL_LABEL_HEIGHT), label, LABEL_FONT)

    # Row labels and image cells.
    for row_idx, (id_name, image_map) in enumerate(rows[:ROWS]):
        y = start_y + COL_LABEL_HEIGHT + row_idx * (cell_size + CELL_GAP)
        label_rect = (start_x, y, start_x + ROW_LABEL_WIDTH, y + cell_size)
        draw.rectangle(label_rect, fill=HEADER_BG)
        draw_centered_text(draw, label_rect, id_name, LABEL_FONT)

        source_prediction = prediction_value(image_map[0]) if 0 in image_map else None

        for col in range(COLS):
            x = start_x + ROW_LABEL_WIDTH + col * (cell_size + CELL_GAP)
            rect = (x, y, x + cell_size, y + cell_size)
            draw.rectangle(rect, fill=SOURCE_BG if col == 0 else CELL_BG)

            image_path = image_map.get(col)
            if image_path is None:
                draw_centered_text(draw, rect, "-", LABEL_FONT, fill=SUBTEXT)
                draw.rectangle(rect, outline=GRID_LINE, width=1)
                continue

            with Image.open(image_path) as img:
                img = img.convert("RGB")
                img.thumbnail((cell_size - 10, cell_size - 10), Image.Resampling.LANCZOS)

                paste_x = x + (cell_size - img.width) // 2
                paste_y = y + (cell_size - img.height) // 2
                canvas.paste(img, (paste_x, paste_y))

            current_prediction = prediction_value(image_path)
            if col == 0:
                border = SOURCE_BORDER
            elif source_prediction is not None and current_prediction != source_prediction:
                border = FAIL_BORDER
            else:
                border = OK_BORDER

            draw.rectangle(rect, outline=border, width=BORDER_WIDTH)

    output_file = OUTPUT_ROOT / f"{safe_filename(experiment_path.name)}_210_images_ppt_grid.png"
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    canvas.save(output_file, quality=95)
    return output_file


def main():
    if not MNIST_PATH.exists():
        raise FileNotFoundError(f"MNIST path not found: {MNIST_PATH}")

    experiments = discover_experiments()
    if not experiments:
        print("No experiment folders found.")
        return

    for experiment_path in experiments:
        output_file = make_slide_grid(experiment_path)
        if output_file is not None:
            print(f"Created: {output_file}")

    print("Done.")


if __name__ == "__main__":
    main()
