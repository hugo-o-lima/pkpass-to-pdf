#!/usr/bin/env python3
import os
import json
import zipfile
import tempfile
import qrcode
from fpdf import FPDF, XPos, YPos
from pathlib import Path


def gerar_pdf(pass_json_path: Path, temp_dir: Path, output_pdf: Path, numero: int):
    with open(pass_json_path, "r", encoding="utf-8") as f:
        dados = json.load(f)

    pdf = FPDF("P", "mm", "A4")
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    pdf.add_font("DejaVu", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    pdf.add_font("DejaVu", "I", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf")

    pdf.set_fill_color(245, 245, 245)
    pdf.rect(10, 10, 190, 277, "F")

    logo_path = temp_dir / "logo.png"
    if logo_path.exists():
        pdf.image(str(logo_path), x=70, y=20, w=70)
    pdf.ln(60)

    pdf.set_font("DejaVu", "B", 18)
    titulo = dados.get("eventTicket", {}).get("primaryFields", [{}])[0].get("value", "Ingresso")
    pdf.multi_cell(180, 12, titulo, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    pdf.set_font("DejaVu", "", 11)
    descricao = dados.get("description", "")
    pdf.multi_cell(180, 8, descricao, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)

    pdf.set_draw_color(180, 180, 180)
    pdf.set_line_width(0.4)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(6)

    def add_info(label, value):
        pdf.multi_cell(180, 8, f"{label}: {value}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    event = dados.get("eventTicket", {})
    pdf.set_font("DejaVu", "B", 14)
    pdf.cell(0, 10, "Detalhes do Evento", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.set_font("DejaVu", "", 12)
    for group in ["headerFields", "secondaryFields", "auxiliaryFields"]:
        for campo in event.get(group, []):
            add_info(campo.get("label", ""), campo.get("value", ""))
    pdf.ln(10)

    # QR Code
    qr_info = None
    if "barcodes" in dados and dados["barcodes"]:
        qr_info = dados["barcodes"][0]
    elif "barcode" in dados:
        qr_info = dados["barcode"]

    if qr_info:
        qr_data = qr_info.get("message", "")
        qr_img = qrcode.make(qr_data)
        qr_temp = temp_dir / "qr_temp.png"
        qr_img.save(qr_temp)

        pdf.set_font("DejaVu", "B", 14)
        pdf.cell(0, 10, "QR Code do Ingresso", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        pdf.image(str(qr_temp), x=70, w=70)
        pdf.ln(80)

        pdf.set_font("DejaVu", "B", 12)
        pdf.multi_cell(180, 8, f"Número do Ingresso: {qr_info.get('altText', '-')}", align="C")

    pdf.set_y(-20)
    pdf.set_font("DejaVu", "I", 9)
    pdf.multi_cell(
        180, 8,
        f"Ingresso gerado automaticamente (ingresso_{numero}) - Hugo Antonio / GitHub",
        align="C"
    )

    pdf.output(str(output_pdf))
    print(f"✅ Gerado: {output_pdf}")


def converter_todos(input_dir: Path, output_dir: Path):
    pkpass_files = sorted(input_dir.glob("*.pkpass"))
    if not pkpass_files:
        print("⚠️ Nenhum arquivo .pkpass encontrado em:", input_dir)
        return

    output_dir.mkdir(exist_ok=True)

    for i, pkpass_file in enumerate(pkpass_files, start=1):
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                with zipfile.ZipFile(pkpass_file, "r") as zip_ref:
                    zip_ref.extractall(temp_dir)

                pass_json = Path(temp_dir) / "pass.json"
                if pass_json.exists():
                    output_pdf = output_dir / f"ingresso_{i}.pdf"
                    gerar_pdf(pass_json, Path(temp_dir), output_pdf, i)
                else:
                    print(f"❌ {pkpass_file.name} não contém pass.json válido.")
            except Exception as e:
                print(f"❌ Erro ao processar {pkpass_file.name}: {e}")

    print(f"\n📂 Conversão concluída! PDFs salvos em: {output_dir}")


if __name__ == "__main__":
    print("🎟️ Conversor PKPASS → PDF\n")

    input_path_str = input("📥 Digite o caminho da pasta com os arquivos .pkpass (ou Enter para usar ~/Downloads): ").strip()
    output_path_str = input("💾 Digite o caminho onde salvar os PDFs (ou Enter para usar ~/Downloads/Ingressos_PDF): ").strip()

    input_path = Path(input_path_str or Path.home() / "Downloads").expanduser()
    output_path = Path(output_path_str or input_path / "Ingressos_PDF").expanduser()

    print(f"\n🔍 Procurando ingressos em: {input_path}")
    print(f"📁 PDFs serão salvos em: {output_path}\n")

    converter_todos(input_path, output_path)
