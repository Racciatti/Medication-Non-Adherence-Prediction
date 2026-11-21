"""Download the NHANES 2013-2014 (cycle H) modules used by this project.

Usage:
    python data/download.py            # saves .xpt files next to this script

Files come from the CDC/NCHS public data server.
"""
import os
import sys
import urllib.request

BASE_URL = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2013/DataFiles/"

FILES = [
    "ALQ_H.xpt", "BPQ_H.xpt", "CBQ_H.xpt", "DEMO_H.xpt", "DIQ_H.xpt",
    "DLQ_H.xpt", "DR1TOT_H.xpt", "DR2TOT_H.xpt", "DS1TOT_H.xpt",
    "DS2TOT_H.xpt", "HUQ_H.xpt", "OSQ_H.xpt", "INQ_H.xpt", "MCQ_H.xpt",
    "PAQ_H.xpt", "PFQ_H.xpt", "RXQ_RX_H.xpt", "SLQ_H.xpt",
]


def download(out_dir: str = os.path.dirname(os.path.abspath(__file__))) -> None:
    """Fetch every file in ``FILES`` into ``out_dir`` (skips existing ones)."""
    os.makedirs(out_dir, exist_ok=True)
    for name in FILES:
        dest = os.path.join(out_dir, name)
        if os.path.exists(dest):
            print(f"skip   {name} (already present)")
            continue
        print(f"fetch  {name}")
        urllib.request.urlretrieve(BASE_URL + name, dest)


if __name__ == "__main__":
    download(*sys.argv[1:2])
