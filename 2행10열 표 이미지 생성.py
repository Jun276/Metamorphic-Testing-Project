import os
import re

from PIL import Image, ImageDraw

# ==================================================
# 사용자 설정
# ==================================================

MNIST_PATH = r"C:\선문대학교\강의\3학년\1학기\전공\소프트웨어품질관리\4. 팀플\팀프로젝트 #2\Metamorphic-Testing-Project\metamorphic_testing\example\mnist"

IMAGE_SIZE = 150

ROWS = 2
COLS = 10

MARGIN = 0

BORDER_WIDTH = 3

# ==================================================
# 생성 대상 ID
#
# None      : 모든 ID 생성
# "ID_1"    : ID_1만 생성
# "ID_5"    : ID_5만 생성
# ==================================================

TARGET_ID = None

# ==================================================
# 출력 폴더
# ==================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

OUTPUT_ROOT = os.path.join(
    SCRIPT_DIR,
    "표이미지"
)

os.makedirs(
    OUTPUT_ROOT,
    exist_ok=True
)

# ==================================================
# 실험 폴더 순회
# ==================================================

for experiment_folder in os.listdir(MNIST_PATH):

    experiment_path = os.path.join(
        MNIST_PATH,
        experiment_folder
    )

    if not os.path.isdir(experiment_path):
        continue

    # 타임스탬프 제거
    experiment_name = re.sub(
        r"\(\d+\)$",
        "",
        experiment_folder
    ).strip()

    print(f"\n실험 처리 중: {experiment_name}")

    # 실험별 출력 폴더
    experiment_output_dir = os.path.join(
        OUTPUT_ROOT,
        experiment_name
    )

    os.makedirs(
        experiment_output_dir,
        exist_ok=True
    )

    # ==================================================
    # ID 폴더 순회
    # ==================================================

    for target_id in os.listdir(experiment_path):

        id_path = os.path.join(
            experiment_path,
            target_id
        )

        if not os.path.isdir(id_path):
            continue

        if not target_id.startswith("ID_"):
            continue

        # 특정 ID만 생성
        if TARGET_ID is not None:
            if target_id != TARGET_ID:
                continue

        images = []

        # ==================================================
        # #1 ~ #20 이미지 수집
        # ==================================================

        for filename in os.listdir(id_path):

            if not filename.lower().endswith(".png"):
                continue

            match = re.match(
                r"#(\d+)_",
                filename
            )

            if not match:
                continue

            index = int(match.group(1))

            if 1 <= index <= 20:
                images.append(
                    (index, filename)
                )

        images.sort(
            key=lambda x: x[0]
        )

        if len(images) == 0:
            print(f"이미지 없음: {target_id}")
            continue

        if len(images) != 20:
            print(
                f"경고: {experiment_name} / {target_id} "
                f"이미지 개수 = {len(images)}"
            )

        # ==================================================
        # 캔버스 생성
        # ==================================================

        canvas_width = (
            COLS * IMAGE_SIZE
            + (COLS + 1) * MARGIN
        )

        canvas_height = (
            ROWS * IMAGE_SIZE
            + (ROWS + 1) * MARGIN
        )

        canvas = Image.new(
            "RGB",
            (canvas_width, canvas_height),
            "white"
        )

        draw = ImageDraw.Draw(canvas)

        # ==================================================
        # 이미지 배치
        # ==================================================

        for idx, (_, filename) in enumerate(images):

            row = idx // COLS
            col = idx % COLS

            x = (
                MARGIN
                + col * (IMAGE_SIZE + MARGIN)
            )

            y = (
                MARGIN
                + row * (IMAGE_SIZE + MARGIN)
            )

            img_path = os.path.join(
                id_path,
                filename
            )

            img = Image.open(
                img_path
            ).convert("RGB")

            img = img.resize(
                (IMAGE_SIZE, IMAGE_SIZE)
            )

            canvas.paste(
                img,
                (x, y)
            )

            draw.rectangle(
                [
                    x,
                    y,
                    x + IMAGE_SIZE,
                    y + IMAGE_SIZE
                ],
                outline="black",
                width=BORDER_WIDTH
            )

        # ==================================================
        # 저장
        # ==================================================

        output_file = os.path.join(
            experiment_output_dir,
            f"{experiment_name}_{target_id}_grid.png"
        )

        canvas.save(output_file)

        print(
            f"생성 완료: {os.path.basename(output_file)}"
        )

print("\n모든 작업 완료")