#!/usr/bin/env python3
"""Generates Gutschrift (self-billing invoice, Section 14(2) sentence 2 UStG)
PDFs for freelancers who don't issue their own invoices, matching the house
style used for GS-VAN-003. Only ever fill in real, agreed line items -- this
script does not derive quantities from a target total.

Usage: python3 scripts/generate-gutschrift.py <input.json> <output_dir>

Input JSON shape:
{
  "issuerName": "Media WEFILM Group UG (haftungsbeschraenkt)",
  "issuerAddress": ["Gubener Str. 50", "10243 Berlin, Deutschland"],
  "issuerVatId": "USt-IdNr. DE357953727",
  "issuerEmail": "info@leadpioneer.de",
  "documents": [
    {
      "recipientName": "Herrn Rene Morana",
      "recipientAddress": ["Stadelheimerstr. 71", "81549 Muenchen, Deutschland"],
      "recipientEmail": "",
      "iban": "",
      "bic": "",
      "gutschriftNummer": "GS-REN-001",
      "gutschriftDatum": "05.04.2026",
      "leistenderUnternehmer": "Rene Morana (freiberuflich)",
      "leistungszeitraum": "Projekt 1, April 2026",
      "taetigkeit": "Copywriting Cold Emails",
      "items": [
        {"beschreibung": "Copywriting: 4 Cold-Email-Copys + 3 Follow-ups (Projekt 1)", "menge": "1", "satz": "300.00 EUR", "betrag": 300.00}
      ],
      "ustHinweis": "Gemaess Section 19 UStG (Kleinunternehmerregelung) wird keine Umsatzsteuer berechnet.",
      "outputFile": "GS-REN-001.pdf"
    }
  ]
}
"""
import json
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas

def draw_gutschrift(path, issuer, doc):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    x = 20 * mm
    y = height - 20 * mm

    c.setFont("Helvetica", 10)
    c.drawString(x, y, issuer["issuerName"])
    y -= 5 * mm
    for line in issuer["issuerAddress"]:
        c.drawString(x, y, line)
        y -= 5 * mm
    c.drawString(x, y, issuer["issuerVatId"])
    y -= 5 * mm
    c.drawString(x, y, issuer["issuerEmail"])
    y -= 12 * mm

    c.setStrokeColor(colors.HexColor("#c0397a"))
    c.line(x, y, x + 90 * mm, y)
    c.setStrokeColor(colors.black)
    y -= 10 * mm

    c.drawString(x, y, doc["recipientName"])
    y -= 5 * mm
    for line in doc.get("recipientAddress", []):
        c.drawString(x, y, line)
        y -= 5 * mm
    if doc.get("recipientEmail"):
        c.drawString(x, y, doc["recipientEmail"])
        y -= 5 * mm
    if doc.get("iban"):
        c.drawString(x, y, f"IBAN: {doc['iban']}")
        y -= 5 * mm
    if doc.get("bic"):
        c.drawString(x, y, f"BIC/Bank: {doc['bic']}")
        y -= 5 * mm
    y -= 6 * mm

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor("#c0397a"))
    c.drawString(x, y, f"Gut/Rechnungsnummer {doc['gutschriftNummer']}")
    c.setFillColor(colors.black)
    y -= 12 * mm

    c.setFont("Helvetica", 10)
    rows = [
        ("Gutschriftdatum:", doc["gutschriftDatum"]),
        ("Leistender Unternehmer:", doc["leistenderUnternehmer"]),
        ("Leistungszeitraum:", doc["leistungszeitraum"]),
        ("Taetigkeit:", doc["taetigkeit"]),
    ]
    for label, value in rows:
        c.setFont("Helvetica", 9)
        c.drawString(x, y, label)
        c.setFont("Helvetica", 10)
        c.drawString(x + 45 * mm, y, value)
        y -= 7 * mm

    y -= 5 * mm
    table_top = y
    c.setFillColor(colors.HexColor("#c0397a"))
    c.rect(x, y - 6 * mm, 150 * mm, 6 * mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x + 2 * mm, y - 4.3 * mm, "Leistung")
    c.drawRightString(x + 100 * mm, y - 4.3 * mm, "Menge")
    c.drawRightString(x + 125 * mm, y - 4.3 * mm, "Satz")
    c.drawRightString(x + 150 * mm, y - 4.3 * mm, "Betrag")
    c.setFillColor(colors.black)
    y -= 6 * mm

    total = 0.0
    c.setFont("Helvetica", 9)
    for item in doc["items"]:
        y -= 7 * mm
        text = c.beginText(x + 2 * mm, y)
        text.setLeading(10)
        for line in wrap_text(item["beschreibung"], 44):
            text.textLine(line)
        c.drawText(text)
        c.drawRightString(x + 100 * mm, y, str(item["menge"]))
        c.drawRightString(x + 125 * mm, y, item["satz"])
        c.drawRightString(x + 150 * mm, y, f"{item['betrag']:.2f} EUR")
        total += item["betrag"]

    y -= 8 * mm
    c.line(x, y, x + 150 * mm, y)
    y -= 6 * mm
    c.setFont("Helvetica-Bold", 10)
    ust_free = "keine USt. ausgewiesen" if doc.get("ustHinweis") else ""
    c.drawString(x, y, f"Gesamtbetrag ({ust_free}):" if ust_free else "Gesamtbetrag:")
    c.drawRightString(x + 150 * mm, y, f"{total:.2f} EUR")
    y -= 14 * mm

    if doc.get("iban"):
        c.setFont("Helvetica", 9)
        c.drawString(x, y, f"Zahlungsverbindung des leistenden Unternehmers: IBAN {doc['iban']}, BIC/Bank {doc.get('bic', '')}.")
        y -= 8 * mm

    c.setFont("Helvetica", 8)
    note = (f"Hinweis zur Umsatzsteuer: {doc['ustHinweis']} " if doc.get("ustHinweis") else "") + (
        "Hinweis zum Gutschriftverfahren: Diese Abrechnung wurde vom Leistungsempfaenger erstellt, da der "
        "leistende Unternehmer ueber keine eigene Rechnungsstellung verfuegt, und wurde ihm zur Kenntnis "
        "gegeben. Sie gilt gem. Section 14 Abs. 2 Satz 2 UStG als Rechnung des leistenden Unternehmers, "
        "sofern dieser der Ausstellung nicht widerspricht."
    )
    text = c.beginText(x, y)
    text.setLeading(10)
    for line in wrap_text(note, 105):
        text.textLine(line)
    c.drawText(text)

    c.showPage()
    c.save()

def wrap_text(text, width):
    words = text.split()
    lines, current = [], ""
    for w in words:
        if len(current) + len(w) + 1 <= width:
            current = f"{current} {w}".strip()
        else:
            lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines

def main():
    if len(sys.argv) != 3:
        print("Usage: generate-gutschrift.py <input.json> <output_dir>", file=sys.stderr)
        sys.exit(1)
    input_path, output_dir = sys.argv[1], sys.argv[2]
    data = json.load(open(input_path, encoding="utf-8"))
    issuer = {k: data[k] for k in ("issuerName", "issuerAddress", "issuerVatId", "issuerEmail")}
    for doc in data["documents"]:
        out_path = f"{output_dir}/{doc['outputFile']}"
        draw_gutschrift(out_path, issuer, doc)
        print(f"wrote {out_path}")

if __name__ == "__main__":
    main()
