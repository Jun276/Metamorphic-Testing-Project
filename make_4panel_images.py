# -*- coding: utf-8 -*-

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import re
import sys

BASE_DIR = Path("metamorphic_testing") / "example" / "mnist"
OUT_DIR = Path("report_panels")
OUT_DIR.mkdir(exist_ok=True)

# 기본은 ID_1 기준으로 4분할 이미지 생성
# 다른 ID를 쓰고 싶으면 실행할 때: python make_4panel_images.py ID_2
SELECTED_ID = sys.argv[1] if len(sys.argv) > 1 else "ID_1"

PICK_NUMBERS = [0, 1, 10, 20]
LABELS = ["원본", "1회차", "10회차", "20회차"]


def load_font(size=28):
    font_paths = [
        r"C:\Windows\Fonts\malgun.ttf",
        r"C:\Windows\Fonts\malgunbd.ttf",
    ]

    for fp in font_paths:
        if Path(fp).exists():
            return ImageFont.truetype(fp, size)

    return ImageFont.load_default()


def get_step_number(path):
    m = re.search(r"#(\d+)_prediction", path.name)
    if m:
        return int(m.group(1))
    return None


def get_prediction_label(path):
    m = re.search(r"prediction_(\d+)", path.name)
    if m:
        return m.group(1)
    return "?"


def find_image_by_step(id_dir, step):
    images = list(id_dir.glob("*.png"))

    for img in images:
        if get_step_number(img) == step:
            return img

    return None


def resize_to_fit(img, max_size):
    img = img.copy()
    img.thumbnail((max_size, max_size))
    return img


def make_panel(result_dir, id_dir):
    selected_paths = []

    for step in PICK_NUMBERS:
        img_path = find_image_by_step(id_dir, step)
        if img_path is None:
            print(f"[SKIP] {result_dir.name} / {id_dir.name}: #{step} 이미지 없음")
            return
        selected_paths.append(img_path)

    font_title = load_font(34)
    font_label = load_font(26)

    cell_w = 420
    cell_h = 420
    title_h = 70
    label_h = 50

    panel_w = cell_w * 2
    panel_h = title_h + (cell_h + label_h) * 2

    panel = Image.new("RGB", (panel_w, panel_h), "white")
    draw = ImageDraw.Draw(panel)

    title = f"{result_dir.name} - {id_dir.name}"
    draw.text((20, 18), title, fill="black", font=font_title)

    for i, img_path in enumerate(selected_paths):
        row = i // 2
        col = i % 2

        x0 = col * cell_w
        y0 = title_h + row * (cell_h + label_h)

        img = Image.open(img_path).convert("RGB")
        img = resize_to_fit(img, 340)

        pred = get_prediction_label(img_path)
        label = f"{LABELS[i]} / pred={pred}"

        draw.text((x0 + 20, y0 + 10), label, fill="black", font=font_label)

        img_x = x0 + (cell_w - img.width) // 2
        img_y = y0 + label_h + (cell_h - img.height) // 2

        panel.paste(img, (img_x, img_y))

        # 칸 테두리
        draw.rectangle(
            [x0 + 5, y0 + 5, x0 + cell_w - 5, y0 + cell_h + label_h - 5],
            outline="black",
            width=2
        )

    safe_name = result_dir.name.replace("/", "_").replace("\\", "_").replace(":", "_")
    out_path = OUT_DIR / f"{safe_name}_{id_dir.name}_4panel.png"
    panel.save(out_path)
    print(f"[OK] {out_path}")


def main():
    if not BASE_DIR.exists():
        print(f"[ERROR] 폴더가 없습니다: {BASE_DIR}")
        return

    result_dirs = [p for p in BASE_DIR.iterdir() if p.is_dir()]

    if not result_dirs:
        print(f"[ERROR] 결과 폴더가 없습니다: {BASE_DIR}")
        return

    print(f"[INFO] 기준 폴더: {BASE_DIR}")
    print(f"[INFO] 선택 ID: {SELECTED_ID}")
    print(f"[INFO] 출력 폴더: {OUT_DIR}")
    print()

    for result_dir in result_dirs:
        id_dir = result_dir / SELECTED_ID

        if not id_dir.exists():
            print(f"[SKIP] {result_dir.name}: {SELECTED_ID} 없음")
            continue

        make_panel(result_dir, id_dir)

    print()
    print("[DONE] report_panels 폴더를 확인하세요.")


if __name__ == "__main__":
    main()
