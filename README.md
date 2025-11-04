# PKPass to PDF Converter

This project provides a Python-based tool that converts Apple Wallet `.pkpass` files into readable and printable PDF tickets.
Each resulting PDF includes event details, descriptions, and a QR code extracted from the pass file.

The converter can process multiple `.pkpass` files in a batch and offers an interactive mode that lets users specify both input and output folders at runtime.

---

## 1. Overview

Apple Wallet `.pkpass` files are ZIP-based containers used to store digital tickets, boarding passes, and coupons.
Each pass includes a `pass.json` file that describes the content and metadata of the pass, along with logos and other resources.

This script:

* Extracts `.pkpass` files automatically.
* Reads and formats data from `pass.json`.
* Generates a well-structured PDF containing ticket information and QR code.
* Supports batch conversion of all `.pkpass` files within a selected folder.

---

## 2. Features

* Converts one or multiple `.pkpass` files simultaneously.
* Automatically detects and embeds QR codes.
* Interactive CLI: users can choose input and output folders.
* Sequential file naming (`ticket_1.pdf`, `ticket_2.pdf`, …).
* Works on Linux, macOS, and Windows.
* No external API or internet connection required.

---

## 3. Requirements

### Software

* **Python 3.9+**
* **pip** (Python package manager)

### Python dependencies

All dependencies are listed in `requirements.txt`:

```bash
fpdf2>=2.7.8
qrcode[pil]>=7.4.2
```

Install them using:

```bash
pip install -r requirements.txt
```

### Fonts

The script uses **DejaVu Sans** for Unicode support.
These fonts are preinstalled on most Linux systems.
On Windows or macOS, download them from [DejaVu Fonts](https://dejavu-fonts.github.io/) if necessary.

---

## 4. Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/hugo-o-lima/pkpass-to-pdf.git
   cd pkpass-to-pdf
   ```

2. (Optional) Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate        # Linux / macOS
   venv\Scripts\activate           # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## 5. Usage

Run the main script:

```bash
python converter_pkpass_para_pdf.py
```

When executed, the program will prompt for two folders:

```
Enter the folder containing .pkpass files (or press Enter to use ~/Downloads):
Enter the destination folder for generated PDFs (or press Enter to use ~/Downloads/Ingressos_PDF):
```

You can:

* Press **Enter** to use the default paths, or
* Type your own absolute or relative paths.

### Example:

```
Enter the folder containing .pkpass files: /home/user/Documents/Tickets
Enter the destination folder for generated PDFs: /home/user/Documents/Converted_PDFs
```

Once the process completes, you’ll see:

```
✅ Generated: /home/user/Documents/Converted_PDFs/ticket_1.pdf
✅ Generated: /home/user/Documents/Converted_PDFs/ticket_2.pdf
Conversion completed! PDFs saved in: /home/user/Documents/Converted_PDFs
```

---

## 6. Output Format

Each generated PDF contains:

* The event logo (if available).
* Event title and description.
* Details such as date, location, seat, and ticket type.
* A functional QR code containing the original validation URL.
* A footer indicating the conversion source.

Output files are named sequentially:

```
ticket_1.pdf
ticket_2.pdf
ticket_3.pdf
```

The layout is optimized for A4 paper and suitable for printing or digital presentation.

---

## 7. Troubleshooting

| Problem                                      | Cause                              | Solution                                                      |
| -------------------------------------------- | ---------------------------------- | ------------------------------------------------------------- |
| `No .pkpass files found`                     | Input folder is empty or incorrect | Verify that `.pkpass` files exist in the specified folder.    |
| `Missing DejaVuSans.ttf`                     | Font not installed                 | Install DejaVu Sans or update the script to use another font. |
| `Not enough horizontal space to render text` | Outdated `fpdf2` version           | Upgrade with `pip install -U fpdf2`.                          |
| QR code missing                              | Pass doesn’t include QR data       | Some passes use barcodes or lack embedded codes.              |

---

## 8. Example Project Structure

```
pkpass-to-pdf/
├── converter_pkpass_para_pdf.py
├── requirements.txt
├── README.md
└── examples/
    ├── sample.pkpass
    └── output_sample.pdf
```

---

## 9. License

This project is distributed under the **MIT License**, which permits use, modification, and distribution with attribution.

```
MIT License

Copyright (c) 2025 Hugo Antonio

Permission is hereby granted, free of charge, to any person obtaining a copy...
```

Refer to the [LICENSE](LICENSE) file for full details.

---

## 10. Author

**Hugo Antonio de Oliveira Lima**
Bachelor of Computer Science — State University of Maringá (UEM)
Website: [https://hugo-antonio.dev.br](https://hugo-antonio.dev.br)
GitHub: [https://github.com/hugo-o-lima](https://github.com/hugo-o-lima)

---

## 11. Contributing

Contributions, feature ideas, and bug reports are welcome.

To contribute:

1. Fork this repository.
2. Create a new branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit and push your changes.
4. Open a Pull Request explaining the improvements or fixes.

---

## 12. Acknowledgments

This project relies on:

* **fpdf2** for PDF generation
* **qrcode** for QR code creation
* Apple’s **PassKit** format specification

---

