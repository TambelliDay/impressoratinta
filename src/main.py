from tesserocr import PyTessBaseAPI
import fitz  # PyMuPDF
import os
import re
import cv2
import numpy as np

# Configurações
TESSDATA_DIR = r"C:\Users\210036\AppData\Local\Programs\Tesseract-OCR\tessdata"
PASTA_INPUT = "./samples"
PASTA_OUTPUT = "./output"

# Criar pasta de saída se não existir
os.makedirs(PASTA_OUTPUT, exist_ok=True)

HP_STR = "HP Laser MFP 432fdn"
LEXMARK_STR = "Lexmark MS415dn"

def detectar_modelo(texto_total: str):
    t = texto_total.lower()
    if HP_STR.lower() in t:
        return "HP"
    if LEXMARK_STR.lower() in t:
        return "Lexmark"
    return None

def rotate_bound(image, angle):
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    cos = abs(M[0, 0]); sin = abs(M[0, 1])
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    return cv2.warpAffine(image, M, (nW, nH), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

def deskew_hough(caminho_img, canny1=50, canny2=200, max_skew=30):
    img = cv2.imread(caminho_img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(blur, canny1, canny2, L2gradient=True)

    h, w = gray.shape
    min_line_len = max(int(0.35 * w), 80)
    max_line_gap = 20

    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100,
        minLineLength=min_line_len, maxLineGap=max_line_gap)

    angle = 0.0
    if lines is not None and len(lines) > 0:
        angs, weights = [], []
        for x1, y1, x2, y2 in lines[:, 0]:
            a = np.degrees(np.arctan2((y2 - y1), (x2 - x1)))
            if -max_skew <= a <= max_skew:
                length = np.hypot(x2 - x1, y2 - y1)
                angs.append(a)
                weights.append(length)
        if angs:
            angle = np.average(angs, weights=weights)

    corrected = rotate_bound(img, -angle)
    temp_path = caminho_img.replace(".png", "_deskew.png")
    cv2.imwrite(temp_path, corrected)
    return temp_path

def processar_pdf(caminho_pdf):
    nome_arquivo = os.path.basename(caminho_pdf)
    resultado = []

    with PyTessBaseAPI(lang="eng", path=TESSDATA_DIR) as tesseract:
        pdf = fitz.open(caminho_pdf)
        modelo = None

        for pagina_num in range(len(pdf)):
            pagina = pdf[pagina_num]
            pix = pagina.get_pixmap(dpi=400)
            temp_path = f"temp_pag_{pagina_num+1}.png"
            pix.save(temp_path)

            temp_path_proc = deskew_hough(temp_path)
            tesseract.SetImageFile(temp_path_proc)
            texto_pagina = tesseract.GetUTF8Text()

            if not modelo:
                modelo = detectar_modelo(texto_pagina)

            if modelo == "HP":
                contador_life = 0
                for linha in texto_pagina.splitlines():
                    if "Life Remaining" in linha:
                        contador_life += 1
                        match = re.search(r"(\d+)%", linha)

                        if not match:
                            tesseract.SetVariable("tessedit_char_whitelist", "0123456789%")
                            tesseract.SetImageFile(temp_path_proc)
                            numeros_ocr = tesseract.GetUTF8Text().strip()
                            tesseract.SetVariable("tessedit_char_whitelist", "")
                            match = re.search(r"(\d+)%", numeros_ocr)

                        if match:
                            valor = int(match.group(1))
                            if contador_life == 1:
                                tipo_peca = "Toner"
                            elif contador_life == 2:
                                tipo_peca = "Unidade de Imagem"
                            else:
                                tipo_peca = f"Peça #{contador_life}"
                            if valor <= 30:
                                resultado.append(f"⚠ Atenção: '{linha.strip()}' → Comprar {tipo_peca}!")
                        else:
                            resultado.append(f"❌ Erro na leitura: '{linha.strip()}'")

            os.remove(temp_path)
            os.remove(temp_path_proc)

        pdf.close()

    if modelo == "Lexmark":
        resultado.append("ℹ Modelo Lexmark MS415dn detectado — nenhuma lógica aplicada.")
    elif not modelo:
        resultado.append("ℹ Nenhum dos modelos alvo detectado — nenhuma lógica aplicada.")
    elif modelo == "HP" and not resultado:
        resultado.append("✅ Nenhum problema encontrado para HP.")

    caminho_saida = os.path.join(PASTA_OUTPUT, f"{nome_arquivo}.txt")
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write("\n".join(resultado))

    print(f"📄 Processado: {nome_arquivo} → Resultado salvo em {caminho_saida} | Modelo: {modelo}")

# Processar todos os PDFs na pasta
pdfs = [f for f in os.listdir(PASTA_INPUT) if f.lower().endswith(".pdf")]
if not pdfs:
    print("❌ Nenhum PDF encontrado na pasta samples.")
else:
    for pdf in pdfs:
        processar_pdf(os.path.join(PASTA_INPUT, pdf))