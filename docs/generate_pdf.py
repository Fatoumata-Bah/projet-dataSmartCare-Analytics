# docs/generate_pdf.py — convertit les deux rapports Markdown en PDF mis en
# forme (page de titre, sections numerotees, tableaux stylises).
# Lancer depuis la racine du repo : python docs/generate_pdf.py
import os
import sys
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import markdown
from xhtml2pdf import pisa

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(DOCS_DIR, "pdf")

CSS = """
@page {
    size: A4;
    margin: 2.2cm 1.8cm 2.2cm 1.8cm;
    @frame footer_frame {
        -pdf-frame-content: footer_content;
        bottom: 1cm; margin-left: 1.8cm; margin-right: 1.8cm; height: 1cm;
    }
}
body { font-family: Helvetica, Arial, sans-serif; font-size: 10.5pt; color: #222; line-height: 1.45; }

.cover { text-align: center; padding-top: 4cm; }
.cover h1 { font-size: 26pt; color: #1B3A6B; margin-bottom: 0.3cm; }
.cover .subtitle { font-size: 13pt; color: #444; margin-bottom: 1cm; }
.cover .tagline { font-size: 11pt; color: #666; font-style: italic; margin-bottom: 1.5cm; }
.cover .date { font-size: 10pt; color: #888; }

h2 { font-size: 16pt; color: #1B3A6B; border-bottom: 2px solid #1B3A6B; padding-bottom: 4px;
     margin-top: 26px; }
h3 { font-size: 12.5pt; color: #1B3A6B; margin-top: 16px; }
h4 { font-size: 11pt; color: #1B3A6B; margin-top: 12px; }

p { margin: 6px 0; text-align: justify; }
ul, ol { margin: 6px 0 6px 0; padding-left: 20px; }
li { margin-bottom: 5px; }
strong { color: #1B3A6B; }

table { width: 100%; border-collapse: collapse; margin: 10px 0 14px 0; font-size: 9pt; }
th { background-color: #1B3A6B; color: #ffffff; padding: 5px 6px; text-align: left; }
td { padding: 5px 6px; border-bottom: 0.5px solid #cccccc; vertical-align: top; }
tr:nth-child(even) td { background-color: #EAF1FA; }

img { max-width: 100%; margin: 10px 0; }
code { background-color: #f0f0f0; padding: 1px 3px; font-family: Courier, monospace; font-size: 9pt; }
blockquote { color: #555; font-style: italic; border-left: 3px solid #1B3A6B; padding-left: 10px; }
#footer_content { font-size: 8pt; color: #888; text-align: center; }
"""

FOOTER = '<div id="footer_content">PSL-CFX Analytics — <pdf:pagenumber /> / <pdf:pagecount /></div>'


def md_to_body_html(md_path):
    with open(md_path, encoding="utf-8") as f:
        text = f.read()
    # Retire le H1 du markdown (une page de titre custom est deja generee)
    text = re.sub(r"^#\s+.+\n+", "", text, count=1)
    html = markdown.markdown(text, extensions=["tables", "fenced_code"])
    return html


def build_pdf(md_path, title, subtitle, tagline, out_path):
    body_html = md_to_body_html(md_path)
    full_html = f"""
    <html><head><meta charset="utf-8"><style>{CSS}</style></head>
    <body>
    <div class="cover">
        <h1>{title}</h1>
        <div class="subtitle">{subtitle}</div>
        <div class="tagline">{tagline}</div>
        <div class="date">PSL-CFX Analytics — Projet Data Epitech</div>
    </div>
    <div style="page-break-before: always;"></div>
    {body_html}
    {FOOTER}
    </body></html>
    """
    with open(out_path, "wb") as f:
        result = pisa.CreatePDF(full_html, dest=f, path=DOCS_DIR)
    if result.err:
        print(f"ERREUR lors de la generation de {out_path}")
    else:
        print(f"OK {out_path}")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    build_pdf(
        os.path.join(DOCS_DIR, "rapport_technique.md"),
        "Rapport technique",
        "PSL-CFX — Pitié-Salpêtrière / Charles Foix",
        "Sources des données, traitements appliqués, choix et justification des modèles",
        os.path.join(OUT_DIR, "Rapport_technique_PSL-CFX.pdf"),
    )
    build_pdf(
        os.path.join(DOCS_DIR, "rapport_mise_en_place.md"),
        "Rapport de mise en place",
        "PSL-CFX — Pitié-Salpêtrière / Charles Foix",
        "Propositions pour gérer les afflux de patients et se préparer aux crises sanitaires",
        os.path.join(OUT_DIR, "Rapport_mise_en_place_PSL-CFX.pdf"),
    )


if __name__ == "__main__":
    main()
