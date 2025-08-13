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

# Função para processar um PDF
def processar_pdf(caminho_pdf):
    nome_arquivo = os.path.basename(caminho_pdf)
    resultado = []

    with PyTessBaseAPI(lang="por", path=TESSDATA_DIR) as tesseract:
        pdf = fitz.open(caminho_pdf)
        for pagina_num in range(len(pdf)):
            pagina = pdf[pagina_num]
            imagem = pagina.get_pixmap(dpi=300)
            temp_path = f"temp_pag_{pagina_num+1}.png"
            imagem.save(temp_path)

            tesseract.SetImageFile(temp_path)
            texto = tesseract.GetUTF8Text()

            for linha in texto.splitlines():
                if "Life Remaining" in linha:
                    match = re.search(r"(\d+)\%", linha)
                    if match:
                        valor = int(match.group(1))
                        if valor <= 30:
                            resultado.append(f"⚠ Atenção: '{linha.strip()}' → Comprar peça!")
                    else:
                        resultado.append(f"❌ Erro na leitura: '{linha.strip()}'")

            os.remove(temp_path)

    # Salvar resultado no arquivo de saída
    caminho_saida = os.path.join(PASTA_OUTPUT, f"{nome_arquivo}.txt")
    with open(caminho_saida, "w", encoding="utf-8") as f:
        if resultado:
            f.write("\n".join(resultado))
        else:
            f.write("✅ Nenhum problema encontrado.")

    print(f"📄 Processado: {nome_arquivo} → Resultado salvo em {caminho_saida}")

# Processar todos os PDFs na pasta
pdfs = [f for f in os.listdir(PASTA_INPUT) if f.lower().endswith(".pdf")]
if not pdfs:
    print("❌ Nenhum PDF encontrado na pasta samples.")
else:
    for pdf in pdfs:
        processar_pdf(os.path.join(PASTA_INPUT, pdf))
