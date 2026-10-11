"""OCR image-only Science chapter PDFs into page-numbered review transcripts.

This is an extraction aid only. It does not classify answers as verified and
does not call the question-bank importer or modify any database.
"""

from __future__ import annotations

import argparse
import re
import subprocess
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader


def output_name(pdf: Path) -> str:
    return re.sub(r"[^a-z0-9]+", "-", pdf.stem.casefold()).strip("-")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", type=Path, help="Directory for OCR transcripts")
    parser.add_argument(
        "pdfs", type=Path, nargs="+", help="Explicit source PDF paths to process"
    )
    parser.add_argument("--tesseract", default="tesseract", help="Tesseract executable")
    args = parser.parse_args()

    pdfs = sorted(args.pdfs, key=lambda path: path.name.casefold())
    if any(not pdf.is_file() or pdf.suffix.casefold() != ".pdf" for pdf in pdfs):
        parser.error("Every input must be an existing PDF file")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    failures = 0
    for pdf in pdfs:
        reader = PdfReader(str(pdf))
        transcript: list[str] = [
            f"SOURCE_PDF: {pdf.name}",
            f"SOURCE_PATH: {pdf.resolve()}",
            f"PAGE_COUNT: {len(reader.pages)}",
            "NOTE: OCR transcript only; answer verification and chapter mapping remain manual.",
        ]
        for page_number, page in enumerate(reader.pages, start=1):
            transcript.extend(["", f"===== PDF_PAGE {page_number} ====="])
            if not page.images:
                transcript.append("OCR_STATUS: NO_EMBEDDED_PAGE_IMAGE")
                failures += 1
                continue
            page_text: list[str] = []
            for image_number, image_file in enumerate(page.images, start=1):
                try:
                    image = image_file.image.convert("RGB")
                    image_data = BytesIO()
                    image.save(image_data, format="PNG")
                    result = subprocess.run(
                        [args.tesseract, "stdin", "stdout", "--psm", "6"],
                        input=image_data.getvalue(),
                        capture_output=True,
                        check=False,
                    )
                except Exception as exc:  # Keep a source-page audit trail.
                    page_text.append(f"[IMAGE {image_number} OCR ERROR: {exc}]")
                    failures += 1
                    continue
                if result.returncode:
                    error = result.stderr.decode("utf-8", errors="replace").strip()
                    page_text.append(f"[IMAGE {image_number} OCR ERROR: {error}]")
                    failures += 1
                else:
                    page_text.append(
                        result.stdout.decode("utf-8", errors="replace").strip()
                    )
            transcript.extend(page_text or ["OCR_STATUS: EMPTY_OCR"])
        output = args.output_dir / f"{output_name(pdf)}.txt"
        output.write_text("\n".join(transcript) + "\n", encoding="utf-8")
        print(f"{pdf.name}: {len(reader.pages)} pages -> {output}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
