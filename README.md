# Dokumentensortierung

Dieses Python-Skript überwacht ein bestimmtes Verzeichnis auf neue PDF-Dateien und sortiert sie basierend auf vordefinierten Suchbegriffen in entsprechende Unterordner. 

## Einrichtung

1. Kopiere die Datei `config.example.json` und benenne die Kopie um in `config.json`.
2. Öffne die `config.json` und passe die Pfade (`watch_dir`, `default_dir` und `target`) sowie die Suchbegriffe (`patterns`) nach deinen Wünschen an.
3. Starte das Skript:
   ```bash
   python pdf_sorter.py
   ```
   
## Virtuelle Umgebung erstellen (optional, aber empfohlen)

```bash
# Virtuelle Umgebung erstellen
python -m venv .venv

# Aktivieren (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Aktivieren (macOS/Linux)
source .venv/bin/activate
```

## Ablauf

```mermaid
graph TD
    %% Definition der Stile
    classDef start_end fill:#f9f,stroke:#333,stroke-width:2px;
    classDef process fill:#bbf,stroke:#333,stroke-width:1px;
    classDef folder fill:#ffb,stroke:#333,stroke-width:1px;

    %% Ablaufdiagramm
    A([Start: PDF im Ordner 'Rechnungseingang' ablegen]) --> B[Skript liest Text aus PDF]
    B --> C{Entspricht der Text<br>einem Regex-Muster?}
    
    C -- Ja --> D[Verschiebe PDF in passenden Zielordner]
    C -- Nein --> E[Verschiebe PDF in Ordner 'Unsortiert']
    
    D --> F([Zielordner: /Kunde_A oder /Kunde_B])
    E --> G([Fallback-Ordner: /Unsortiert])
    
    %% Klassen zuweisen
    class A start_end;
    class B,C process;
    class F,G folder;
```

