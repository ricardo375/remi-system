import os
import json
from moviepy.editor import VideoFileClip
from pathlib import Path

# UPDATE THIS PATH to match your SSD structure
base_path = Path("/Volumes/Extreme SSD/original media")

video_metadata = []

for root, dirs, files in os.walk(base_path):
    if 'raw' in root.lower():
        for file in files:
            if file.lower().endswith(('.mov', '.mp4', '.m4v')):
                file_path = os.path.join(root, file)
                try:
                    clip = VideoFileClip(file_path)
                    metadata = {
                        "file_path": file_path,
                        "duration_sec": round(clip.duration, 2),
                        "fps": round(clip.fps, 2),
                        "resolution": f"{clip.w}x{clip.h}",
                        "filesize_mb": round(os.path.getsize(file_path) / (1024 * 1024), 2)
                    }
                    video_metadata.append(metadata)
                    clip.close()
                except Exception as e:
                    print(f"❌ Error processing {file_path}: {e}")

# Output results to a JSON file
output_path = "output/video_metadata.json"
os.makedirs("output", exist_ok=True)

with open(output_path, "w") as f:
    json.dump(video_metadata, f, indent=4)

print(f"✅ Done! Metadata saved to: {output_path}")