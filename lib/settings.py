import sys
import os

IS_WIN = True if (
    sys.platform in ["win32", "cygwin"] or os.name == "nt") else False
# Encoding used for Unicode data
UNICODE_ENCODING = "utf-8"
