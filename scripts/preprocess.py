import os
import cv2
import pandas as pd

# =====================================
# SETTINGS
# =====================================
RAW_FOLDER = "../raw_data"
OUTPUT_FOLDER = "../processed_dataset"
FPS = 30  # Change if needed

ALLOWED_CLASSES = ["Pointing", "Writing", "No Gesture"]

# Manually choose which videos are train vs val
TRAIN_VIDEOS = ["Lizbeth_Lozano_1"]
VAL_VIDEOS = ["Musquiz_Science"]

# =====================================
# CREATE OUTPUT FOLDERS
# =====================================
for split in ["train", "val"]:
    for cls in ALLOWED_CLASSES:
        os.makedirs(os.path.join(OUTPUT_FOLDER, split, cls), exist_ok=True)

# =====================================
# TIME CONVERSION FUNCTION
# =====================================
def time_to_seconds(time_str):
    h, m, s = time_str.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)

# =====================================
# PROCESS EACH EXCEL FILE
# =====================================
for file in os.listdir(RAW_FOLDER):
    if not file.endswith(".xlsx"):
        continue

    base_name = file.replace(".xlsx", "")
    video_path = os.path.join(RAW_FOLDER, base_name + ".mp4")
    excel_path = os.path.join(RAW_FOLDER, file)

    if not os.path.exists(video_path):
        print(f"Skipping {base_name} (no matching video)")
        continue

    # Decide split
    if base_name in TRAIN_VIDEOS:
        split = "train"
    elif base_name in VAL_VIDEOS:
        split = "val"
    else:
        print(f"Skipping {base_name} (not assigned to train or val)")
        continue

    print(f"Processing {base_name} → {split}")

    # =====================================
    # LOAD EXCEL
    # =====================================
    df = pd.read_excel(excel_path)

    # Clean behavior column
    df["Behavior"] = (
        df["Behavior"]
        .astype(str)
        .str.strip()
    )

    # Keep only the 3 classes
    df = df[df["Behavior"].isin(ALLOWED_CLASSES)]

    # Sort by time
    df = df.sort_values("Time_Relative_hms")

    # Debug print (optional)
    print(df["Behavior"].value_counts())

    cap = cv2.VideoCapture(video_path)

    active_start = {}

    # =====================================
    # LOOP THROUGH EVENTS
    # =====================================
    for _, row in df.iterrows():
        behavior = row["Behavior"]
        event = row["Event_Type"]
        time_str = row["Time_Relative_hms"]

        seconds = time_to_seconds(time_str)
        frame_num = int(seconds * FPS)

        if event == "State start":
            active_start[behavior] = frame_num

        elif event == "State stop" and behavior in active_start:
            start_frame = active_start.pop(behavior)
            end_frame = frame_num

            for f in range(start_frame, end_frame + 1):
                cap.set(cv2.CAP_PROP_POS_FRAMES, f)
                ret, frame = cap.read()
                if not ret:
                    break

                save_path = os.path.join(
                    OUTPUT_FOLDER,
                    split,
                    behavior,
                    f"{base_name}_{f:06d}.jpg"
                )

                cv2.imwrite(save_path, frame)

    cap.release()

print("Preprocessing complete.")