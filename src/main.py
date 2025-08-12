from tesserocr import PyTessBaseAPI
import fitz  # PyMuPDF
import os
import re

TESSDATA_DIR = r"C:\Users\210036\AppData\Local\Programs\Tesseract-OCR\tessdata"

pdf = fitz.open("./samples/HP 432 MFP.pdf")

with PyTessBaseAPI(lang="por", path=TESSDATA_DIR) as tesseract:
    for pagina_num in range(len(pdf)):
        pagina = pdf[pagina_num]
        imagem = pagina.get_pixmap(dpi=300)
        temp_path = f"temp_pag_{pagina_num+1}.png"
        imagem.save(temp_path)

        tesseract.SetImageFile(temp_path)
        texto = tesseract.GetUTF8Text()

        print(f"\n--- Página {pagina_num+1} ---")
        print(texto)

        # Procurar todos os "Life Remaining"
        for linha in texto.splitlines():
            if "Life Remaining" in linha:
                match = re.search(r"(\d+)\%", linha)
                if match:
                    valor = int(match.group(1))
                    if valor <= 30:
                        print(f"⚠ Atenção: '{linha.strip()}' → Comprar peça!")
                else:
                    print(f"❌ Erro na leitura: '{linha.strip()}'")

        os.remove(temp_path)
