#!/usr/bin/env python3
"""Generates GoBD-style Eigenbeleg PDFs for transactions with no external
receipt (e.g. payment-provider cashback/fee rebates), one PDF per group.

Usage: python3 scripts/generate-eigenbeleg.py <input.json> <output_dir>

Input JSON shape:
{
  "issuer": "Media WEFILM Group UG (haftungsbeschraenkt)",
  "preparedBy": "Benjamin Diaby",
  "reason": "Freitext-Begruendung, warum kein externer Beleg vorliegt und was gebucht wird.",
  "account": "Nebenkosten des Geldverkehrs",
  "groups": [
    { "belegNummer": "EB-2025-04", "date": "2025-04-03", "lines": [0.35] }
  ]
}
"""
import json
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import date

def draw_eigenbeleg(path, issuer, prepared_by, reason, account, beleg_nummer, beleg_date, lines):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    x = 20 * mm
    y = height - 25 * mm

    c.setFont("Helvetica-Bold", 18)
    c.drawString(x, y, "Eigenbeleg")
    c.setFont("Helvetica", 9)
    c.drawRightString(width - 20 * mm, y, f"Beleg-Nr. {beleg_nummer}")
    y -= 6 * mm
    c.line(x, y, width - 20 * mm, y)
    y -= 10 * mm

    c.setFont("Helvetica-Bold", 10)
    c.drawString(x, y, "Aussteller:")
    c.setFont("Helvetica", 10)
    c.drawString(x + 35 * mm, y, issuer)
    y -= 6 * mm

    c.setFont("Helvetica-Bold", 10)
    c.drawString(x, y, "Belegdatum:")
    c.setFont("Helvetica", 10)
    c.drawString(x + 35 * mm, y, beleg_date)
    y -= 6 * mm

    c.setFont("Helvetica-Bold", 10)
    c.drawString(x, y, "Erstellt von:")
    c.setFont("Helvetica", 10)
    c.drawString(x + 35 * mm, y, prepared_by)
    y -= 6 * mm

    c.setFont("Helvetica-Bold", 10)
    c.drawString(x, y, "Erstellt am:")
    c.setFont("Helvetica", 10)
    c.drawString(x + 35 * mm, y, date.today().strftime("%d.%m.%Y"))
    y -= 10 * mm

    c.setFont("Helvetica-Bold", 10)
    c.drawString(x, y, "Grund:")
    y -= 5 * mm
    c.setFont("Helvetica", 9)
    text = c.beginText(x, y)
    text.setLeading(12)
    for line in wrap_text(reason, 100):
        text.textLine(line)
    c.drawText(text)
    y = text.getY() - 8 * mm

    c.setFont("Helvetica-Bold", 10)
    c.drawString(x, y, "Einzelbuchungen laut Kontoauszug:")
    y -= 7 * mm

    c.setFont("Helvetica-Bold", 9)
    c.drawString(x, y, "Datum")
    c.drawRightString(x + 90 * mm, y, "Betrag (EUR)")
    y -= 2 * mm
    c.line(x, y, x + 90 * mm, y)
    y -= 5 * mm

    c.setFont("Helvetica", 9)
    total = 0.0
    for amount in lines:
        c.drawString(x, y, beleg_date)
        c.drawRightString(x + 90 * mm, y, f"{amount:.2f}")
        total += amount
        y -= 5 * mm

    y -= 2 * mm
    c.line(x, y, x + 90 * mm, y)
    y -= 6 * mm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x, y, "Summe")
    c.drawRightString(x + 90 * mm, y, f"{total:.2f} EUR")
    y -= 12 * mm

    c.setFont("Helvetica-Bold", 10)
    c.drawString(x, y, "Buchungskonto:")
    c.setFont("Helvetica", 10)
    c.drawString(x + 35 * mm, y, f"{account} (Minderung / Ausgabenminderung)")
    y -= 10 * mm

    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(colors.grey)
    note = ("Dieser Eigenbeleg ersetzt gemaess GoBD einen externen Beleg, da der "
            "Zahlungsdienstleister fuer diese Gutschrift keinen Einzelbeleg ausstellt. "
            "Grundlage ist der Kontoauszug des Geschaeftskontos.")
    text = c.beginText(x, y)
    text.setLeading(10)
    for line in wrap_text(note, 110):
        text.textLine(line)
    c.drawText(text)
    c.setFillColor(colors.black)

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
        print("Usage: generate-eigenbeleg.py <input.json> <output_dir>", file=sys.stderr)
        sys.exit(1)
    input_path, output_dir = sys.argv[1], sys.argv[2]
    data = json.load(open(input_path, encoding="utf-8"))
    for group in data["groups"]:
        out_path = f"{output_dir}/{group['belegNummer']}.pdf"
        draw_eigenbeleg(
            out_path,
            data["issuer"],
            data["preparedBy"],
            data["reason"],
            data["account"],
            group["belegNummer"],
            group["date"],
            group["lines"],
        )
        print(f"wrote {out_path}")

if __name__ == "__main__":
    main()
