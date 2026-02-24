import os 
import pandas as pd 

RAW_FOLDER = "/Users/alesia/projects/lltlab/gmlpreprocessing/raw_data"
FPS = 30

ALLOWED_CLASSES = ["Pointing", "Writing", "No Gesture"]

OUTPUT_FILE = "Cleaned_annotations.csv"

def time_to_seconds(time_value):
    # If it's already a timedelta
    if hasattr(time_value, "total_seconds"):
        return time_value.total_seconds()
    
    # If it's a string (fallback)
    if isinstance(time_value, str):
        h, m, s = time_value.split(":")
        return int(h)*3600 + int(m)*60 + float(s)

    # If it's numeric (unlikely but safe)
    return float(time_value)

all_annotations = []

for file in os.listdir(RAW_FOLDER):
    if not file.endswith(".xlsx"):
        continue

    base_name = file.replace(".xlsx", "")
    excel_path = os.path.join(RAW_FOLDER, file)

    print(f"Checking {base_name}")

    df = pd.read_excel(excel_path)

    # Clean Behavior column
    df["Behavior"] = df["Behavior"].astype(str).str.strip()

    # Keep only desired gestures
    df = df[df["Behavior"].isin(ALLOWED_CLASSES)]

    # Sort by time
    df = df.sort_values("Time_Relative_hms")

    active_start = {}

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

            all_annotations.append({
                "video": base_name,
                "behavior": behavior,
                "start_frame": start_frame,
                "end_frame": end_frame
            })

# Save to CSV
annotations_df = pd.DataFrame(all_annotations)
annotations_df.to_csv(OUTPUT_FILE, index=False)

print("\nVerification complete.")
print(f"Saved: {OUTPUT_FILE}")
print("\nPreview:")
print(annotations_df.head())
print("\nUnique Behavior values BEFORE filtering:")
print(df["Behavior"].unique()) 