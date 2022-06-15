import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = os.path.join(BASE_DIR, 'invoice_manager/attachments/')
