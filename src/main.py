from tesserocr import PyTessBaseAPI
import fitz  # PyMuPDF
import os
import re

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

def processar_pdf(caminho_pdf):
    nome_arquivo = os.path.basename(caminho_pdf)
    resultado = []

    # OCR de todas as páginas para um único bloco de texto
    with PyTessBaseAPI(lang="por", path=TESSDATA_DIR) as tesseract:
        pdf = fitz.open(caminho_pdf)
        texto_total = ""
        for pagina_num in range(len(pdf)):
            pagina = pdf[pagina_num]
            pix = pagina.get_pixmap(dpi=300)
            temp_path = f"temp_pag_{pagina_num+1}.png"
            pix.save(temp_path)

            tesseract.SetImageFile(temp_path)
            texto_total += tesseract.GetUTF8Text() + "\n"

            os.remove(temp_path)
        pdf.close()

    # Detectar modelo por substring exata (case-insensitive)
    modelo = detectar_modelo(texto_total)

    if modelo == "HP":
        # Aplica a lógica apenas para HP
        for linha in texto_total.splitlines():
            if "Life Remaining" in linha:
                match = re.search(r"(\d+)\%", linha)
                if match:
                    valor = int(match.group(1))
                    if valor <= 30:
                        resultado.append(f"⚠ Atenção: '{linha.strip()}' → Comprar peça!")
                else:
                    resultado.append(f"❌ Erro na leitura: '{linha.strip()}'")
        if not resultado:
            resultado.append("✅ Nenhum problema encontrado para HP.")
    elif modelo == "Lexmark":
        # Lexmark detectado → não aplicar lógica
        resultado.append("ℹ Modelo Lexmark MS415dn detectado — nenhuma lógica aplicada.")
    else:
        # Nenhum modelo detectado → não aplicar lógica
        resultado.append("ℹ Nenhum dos modelos alvo detectado — nenhuma lógica aplicada.")

    # Salvar resultado no arquivo de saída
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