import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
QUERY_LOG = os.path.join(LOG_DIR, "query_log.txt")
EVAL_LOG = os.path.join(LOG_DIR, "eval_log.txt")
os.makedirs(LOG_DIR, exist_ok=True) # make sure logs dir exists

def log_entry(question, answer, sources):
    with open(QUERY_LOG, "a", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write(f"Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Query     : {question}\n")
        f.write(f"Response  : {answer}\n")
        f.write(f"Sources   : {', '.join(sources)}\n")
        f.write("=" * 60 + "\n\n")

def start_eval_log(question, answer, sources):
    with open(EVAL_LOG, "a", encoding="utf-8") as f:
        f.write("\n")
        f.write("=" * 60 + "\n")
        f.write(f"Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Query     : {question}\n")
        f.write(f"Response  : {answer}\n")
        f.write(f"Sources   : {', '.join(sources)}\n")

def eval_log_entry(message):
    with open(EVAL_LOG, "a", encoding="utf-8") as f:
        f.write(message + "\n")