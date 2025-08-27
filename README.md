# 📄 OCR Printer Analyzer

Este projeto realiza **processamento de PDFs gerados por impressoras** utilizando **OCR (Tesseract)** e técnicas de **processamento de imagens** com OpenCV.
Ele identifica o modelo da impressora (HP ou Lexmark) e analisa os relatórios para verificar o nível de toner, unidade de imagem e outros consumíveis, gerando um relatório textual simplificado.

---

## ⚙️ Funcionalidades

* Detecta automaticamente o modelo da impressora no relatório (`HP Laser MFP 432fdn` ou `Lexmark MS415dn`).
* Realiza **deskew** (correção de inclinação) em páginas escaneadas usando transformada de Hough.
* Para relatórios **HP**:

  * Extrai valores de **Life Remaining (%)**.
  * Aponta quando toner ou unidade de imagem estão abaixo de 30%.
* Para relatórios **Lexmark**:

  * Detecta barras de status em “suprimentos”.
  * Indica se o nível está OK ou baixo (com base em análise de pixels binarizados).
* Gera um relatório em `.txt` com os resultados.
* Processa todos os PDFs presentes na pasta `./samples`.

---

## 🛠️ Tecnologias utilizadas

* [Python 3.x](https://www.python.org/)
* [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) – extração de páginas dos PDFs
* [tesserocr](https://github.com/sirfz/tesserocr) – interface para o Tesseract OCR
* [OpenCV](https://opencv.org/) – deskew e análise de imagens
* [NumPy](https://numpy.org/) – operações matriciais
* [Regex (re)](https://docs.python.org/3/library/re.html) – extração de valores percentuais

---

## 📂 Estrutura do Projeto

```
.
├── samples/        # PDFs de entrada
├── output/         # Relatórios gerados
├── main.py         # Código principal
└── README.md
```

---

## 🚀 Como usar

### 1. Instale as dependências

```bash
pip install tesserocr pymupdf opencv-python numpy
```

⚠️ É necessário ter o [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) instalado na máquina.
No Windows, configure o caminho da pasta `tessdata` em:

```python
TESSDATA_DIR = r"C:\Users\SeuUsuario\AppData\Local\Programs\Tesseract-OCR\tessdata"
```

---

### 2. Coloque os PDFs de relatório na pasta `samples/`

### 3. Execute o script

```bash
python main.py
```

### 4. Veja os resultados em `output/`

Cada relatório analisado gera um `.txt` com informações sobre toner e unidades de imagem.

---

## 📊 Exemplo de saída

### HP

```
⚠ Atenção: 'Toner Life Remaining: 25%' → Comprar Toner!
✅ Unidade de Imagem em nível aceitável
```

### Lexmark

```
✅ Toner em nível ok
⚠ Atenção: Unidade de Imagem com nível baixo (barra preta detectada)
```

---

## 📌 Possíveis melhorias

* Suporte a novos modelos de impressoras.
* Exportar resultados em formato **JSON** para integração com APIs.
* Interface gráfica simples (PyQt/Tkinter).
* Deploy como serviço web (Flask/FastAPI).

---
