

from roboflow import Roboflow
from pathlib import Path

API_KEY    = "jHi93YoP2YZo9tVYZtil"
OUTPUT_DIR = Path(r"C:\SWOS\module1_detection\data\roboflow_hazardous")

rf = Roboflow(api_key=API_KEY)

# Fix for Windows BadZipFile bug — use curl download instead
project = rf.workspace("leo-ueno").project("garbage-classification-3")
version = project.version(1)

# Get download URL directly
url = version.generate_download_url(model_format="yolov8", stub=False)
print(f"\nDownload URL: {url}")
print("\nNow run the curl command printed above")