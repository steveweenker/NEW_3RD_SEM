import asyncio
import os
import time
import aiohttp
import zipfile
import pytz
from io import BytesIO
from datetime import datetime
from typing import Optional, List

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
URL = "https://results.beup.ac.in/BTech3rdSem2024_B2023Results.aspx"

CHECK_INTERVAL = 2
CONTINUOUS_DURATION = 900
SCHEDULED_INTERVAL = 5

RESULT_URLS = [
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2022Pub.aspx?Sem=III&RegNo=22156148040",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148028",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148002",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148001",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148003",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148005",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148006",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148009",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148010",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148013",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148016",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148017",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148018",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148020",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148021",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148022",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148023",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148024",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148025",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148026",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148027",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148028",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148029",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148030",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148031",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148032",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148034",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148001",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148002",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148003",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148005",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148006",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148007",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148008",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148009",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148010",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148011",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148012",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148014",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148015",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148017",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148018",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148019",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148020",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148022",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148023",
    # 23101148001 - 23101148060
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148001",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148002",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148003",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148004",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148005",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148006",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148007",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148008",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148009",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148010",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148011",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148012",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148013",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148014",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148015",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148016",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148017",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148018",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148019",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148020",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148021",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148022",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148023",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148024",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148025",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148026",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148027",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148028",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148029",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148030",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148031",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148032",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148033",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148034",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148035",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148036",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148037",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148038",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148039",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148040",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148041",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148042",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148043",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148044",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148045",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148046",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148047",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148048",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148049",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148050",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148051",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148052",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148053",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148054",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148055",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148056",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148057",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148058",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148059",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23101148060",
    # 24101148901 - 24101148930
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148901",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148902",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148903",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148904",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148905",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148906",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148907",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148908",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148909",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148910",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148911",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148912",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148913",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148914",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148915",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148916",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148917",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148918",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148919",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148920",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148921",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148922",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148923",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148924",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148925",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148926",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148927",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148928",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148929",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24101148930",
    # 23102148001 - 23102148060
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148001",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148002",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148003",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148004",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148005",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148006",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148007",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148008",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148009",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148010",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148011",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148012",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148013",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148014",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148015",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148016",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148017",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148018",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148019",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148020",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148021",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148022",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148023",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148024",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148025",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148026",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148027",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148028",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148029",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148030",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148031",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148032",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148033",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148034",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148035",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148036",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148037",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148038",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148039",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148040",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148041",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148042",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148043",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148044",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148045",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148046",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148047",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148048",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148049",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148050",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148051",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148052",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148053",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148054",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148055",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148056",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148057",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148058",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148059",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23102148060",
    # 24102148901 - 24102148930
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148901",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148902",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148903",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148904",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148905",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148906",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148907",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148908",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148909",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148910",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148911",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148912",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148913",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148914",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148915",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148916",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148917",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148918",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148919",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148920",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148921",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148922",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148923",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148924",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148925",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148926",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148927",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148928",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148929",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24102148930",
    # 23104148001 - 23104148060
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148001",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148002",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148003",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148004",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148005",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148006",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148007",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148008",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148009",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148010",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148011",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148012",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148013",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148014",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148015",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148016",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148017",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148018",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148019",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148020",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148021",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148022",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148023",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148024",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148025",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148026",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148027",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148028",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148029",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148030",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148031",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148032",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148033",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148034",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148035",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148036",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148037",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148038",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148039",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148040",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148041",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148042",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148043",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148044",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148045",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148046",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148047",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148048",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148049",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148050",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148051",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148052",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148053",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148054",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148055",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148056",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148057",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148058",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148059",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23104148060",
    # 24104148901 - 24104148930
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148901",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148902",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148903",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148904",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148905",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148906",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148907",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148908",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148909",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148910",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148911",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148912",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148913",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148914",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148915",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148916",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148917",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148918",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148919",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148920",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148921",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148922",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148923",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148924",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148925",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148926",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148927",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148928",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148929",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=24104148930"
]

class DiscordMonitor:
    def __init__(self):
        self.last_status: Optional[str] = None
        self.last_scheduled_time: float = 0
        self.rate_limit_remaining = 5
        self.rate_limit_reset = 0
        self.ist_timezone = pytz.timezone('Asia/Kolkata')

    def get_indian_time(self) -> str:
        """Get current Indian time in IST timezone using pytz"""
        utc_now = datetime.now(pytz.utc)
        ist_now = utc_now.astimezone(self.ist_timezone)
        return ist_now.strftime("%d-%m-%Y %I:%M:%S %p IST")

    async def send_discord_message(self, content: str, username: str = "BEUP Monitor") -> bool:
        if not DISCORD_WEBHOOK_URL:
            return False
        now = time.time()
        if self.rate_limit_remaining <= 0 and now < self.rate_limit_reset:
            await asyncio.sleep(self.rate_limit_reset - now)
        payload = {"content": content, "username": username}
        async with aiohttp.ClientSession() as session:
            async with session.post(DISCORD_WEBHOOK_URL, json=payload) as resp:
                self.rate_limit_remaining = int(resp.headers.get("X-RateLimit-Remaining", 5))
                reset_after = resp.headers.get("X-RateLimit-Reset-After")
                if reset_after:
                    self.rate_limit_reset = now + float(reset_after)
                if resp.status == 429:
                    retry = float(resp.headers.get("retry-after", 1))
                    await asyncio.sleep(retry)
                    return await self.send_discord_message(content, username)
                return resp.status in (200, 204)

    async def send_file(self, filename: str, data: BytesIO) -> bool:
        form = aiohttp.FormData()
        data.seek(0)
        ctype = "application/zip" if filename.endswith(".zip") else "text/html"
        form.add_field("file", data, filename=filename, content_type=ctype)
        async with aiohttp.ClientSession() as session:
            async with session.post(DISCORD_WEBHOOK_URL, data=form) as resp:
                now = time.time()
                self.rate_limit_remaining = int(resp.headers.get("X-RateLimit-Remaining", 5))
                reset_after = resp.headers.get("X-RateLimit-Reset-After")
                if reset_after:
                    self.rate_limit_reset = now + float(reset_after)
                if resp.status == 429:
                    retry = float(resp.headers.get("retry-after", 1))
                    await asyncio.sleep(retry)
                    return await self.send_file(filename, data)
                return resp.status in (200, 204)

    async def check_site(self) -> str:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(URL, timeout=10) as resp:
                    return "UP" if resp.status == 200 else "DOWN"
        except:
            return "DOWN"

    async def download_and_zip(self) -> BytesIO:
        buffer = BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            async with aiohttp.ClientSession() as session:
                for idx, url in enumerate(RESULT_URLS, start=1):
                    reg = url.split("=")[-1]
                    try:
                        async with session.get(url, timeout=10) as resp:
                            if resp.status == 200:
                                html = await resp.text()
                                zf.writestr(f"result_{reg}.html", html)
                    except Exception:
                        pass
                    if idx % 10 == 0 or idx == len(RESULT_URLS):
                        current_time = self.get_indian_time()
                        await self.send_discord_message(f"🔄 Downloaded & added to ZIP: {idx}/{len(RESULT_URLS)} - {current_time}")
        buffer.seek(0)
        return buffer

    async def continuous_status(self):
        end = time.time() + CONTINUOUS_DURATION
        while time.time() < end:
            left = int(end - time.time())
            current_time = self.get_indian_time()
            await self.send_discord_message(f"✅ Website still UP ({left}s left) - {current_time}")
            await asyncio.sleep(CHECK_INTERVAL)

    async def run(self):
        start_time = self.get_indian_time()
        await self.send_discord_message(f"🔍 Monitoring started at {start_time}")
        while True:
            current = await self.check_site()
            now = time.time()
            changed = current != self.last_status
            scheduled_due = (now - self.last_scheduled_time) >= SCHEDULED_INTERVAL

            if changed:
                current_time = self.get_indian_time()
                if current == "UP":
                    await self.send_discord_message(f"🎉 WEBSITE IS NOW LIVE! - {current_time}")
                    await self.send_discord_message("Starting download…")
                    zip_data = await self.download_and_zip()
                    if await self.send_file("results.zip", zip_data):
                        upload_time = self.get_indian_time()
                        await self.send_discord_message(f"📥 Uploaded all {len(RESULT_URLS)} results as ZIP - {upload_time}")
                    else:
                        await self.send_discord_message("⚠️ ZIP upload failed; sending individual files")
                        async with aiohttp.ClientSession() as session:
                            for idx, url in enumerate(RESULT_URLS, start=1):
                                reg = url.split("=")[-1]
                                try:
                                    async with session.get(url, timeout=10) as resp:
                                        if resp.status == 200:
                                            bio = BytesIO((await resp.text()).encode("utf-8"))
                                            await self.send_file(f"result_{reg}.html", bio)
                                except:
                                    pass
                                if idx % 10 == 0 or idx == len(RESULT_URLS):
                                    current_time = self.get_indian_time()
                                    await self.send_discord_message(f"🔄 Fallback uploaded {idx}/{len(RESULT_URLS)} - {current_time}")
                        upload_time = self.get_indian_time()
                        await self.send_discord_message(f"📥 Individual files uploaded - {upload_time}")
                    self.last_scheduled_time = now
                    await self.continuous_status()
                    # At end of continuous, send immediate scheduled update
                    end_time = self.get_indian_time()
                    await self.send_discord_message(f"📅 Scheduled update: Website is UP - {end_time}")
                    self.last_scheduled_time = time.time()
                else:
                    await self.send_discord_message(f"🔴 WEBSITE IS DOWN - {current_time}")
                    self.last_scheduled_time = now

            elif scheduled_due:
                current_time = self.get_indian_time()
                emoji = "✅" if current == "UP" else "🔴"
                await self.send_discord_message(f"{emoji} Scheduled update: Website is {current} - {current_time}")
                self.last_scheduled_time = now

            self.last_status = current
            await asyncio.sleep(CHECK_INTERVAL)

async def main():
    monitor = DiscordMonitor()
    try:
        await monitor.run()
    except Exception as e:
        import traceback
        error_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d-%m-%Y %I:%M:%S %p IST")
        print(f"❌ Exception in monitor at {error_time}:", e)
        traceback.print_exc()
        raise

if __name__ == "__main__":
    asyncio.run(main())
