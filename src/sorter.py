import json
import re
import shutil
from pathlib import Path
from pypdf import PdfReader


CONFIG_FILE = Path(__file__).parent / "config.json"
EXAMPLE_CONFIG_FILE = Path(__file__).parent / "config.example.json"

def load_config():
    if not CONFIG_FILE.exists():
        if EXAMPLE_CONFIG_FILE.exists():
            print("Information: 'config.json' wurde nicht gefunden.")
            print("Erstelle eine neue 'config.json' basierend auf 'config.example.json'...")
            shutil.copy(EXAMPLE_CONFIG_FILE, CONFIG_FILE)
            print("-> Bitte öffne die neue 'config.json' und passe deine Pfade an")
        else:
            raise FileNotFoundError(
                "Weder 'config.json' noch 'config.example.json' wurden gefunden"
            )
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)

    return {
        "watch_dir": Path(config["watch_dir"]),
        "default_dir": Path(config["default_dir"]),
        "rules": [
            {
                "name": r["name"],
                "target": Path(r["target"]),
                "patterns": r["patterns"]
            }
            for r in config["rules"]
        ]
    }

def process_pdfs():
    try:
        cfg = load_config()
    except Exception as e:
        print(f"Konfigurationsfehler: {e}")
        return

    for pdf_path in cfg["watch_dir"].glob("*.pdf"):
        try:
            reader = PdfReader(pdf_path)
            text = "".join([page.extract_text() for page in reader.pages])

            moved = False
            for rule in cfg["rules"]:
                if any(re.search(pattern, text, re.IGNORECASE) for pattern in rule["patterns"]):
                    rule["target"].mkdir(parents=True, exist_ok=True)
                    pdf_path.rename(rule["target"] / pdf_path.name)
                    moved = True
                    break

            if not moved:
                cfg["default_dir"].mkdir(parents=True, exist_ok=True)
                pdf_path.rename(cfg["default_dir"] / pdf_path.name)
                print(f"Einsortiert nach 'Unsortiert': {pdf_path.name}")

        except Exception as e:
            print(f"Fehler bei Datei {pdf_path.name}: {e}")

if __name__ == "__main__":
    process_pdfs()