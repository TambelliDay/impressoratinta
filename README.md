

# Análise de Relatórios de Impressoras

Este projeto é desenvolvido para automatizar a análise de relatórios em PDF das impressoras **HP 432 MFP** e **Lexmark 415dn**.
Ele identifica automaticamente quais impressoras precisam de **toner** ou **unidade de imagem**, gerando um relatório em texto já no formato pré-programado para solicitação de suprimentos.

---

## 🚀 Funcionalidades

* 📂 Leitura de relatórios **PDF** gerados pelas impressoras.
* 🔍 Identificação automática de impressoras que precisam de **toner** ou **unidade de imagem**.

---

## 🖨️ Modelos Compatíveis

* **HP 432 MFP**
* **Lexmark 415dn**

---

## 📋 Pré-requisitos

* Python **3.8+**
* Bibliotecas necessárias:

  ```bash
  pip install -r requirements.txt
  ```

---

## ⚙️ Como Usar

1. Coloque seus PDFs na pasta `samples/`.
2. Execute o script:

   ```bash
   python src/main.py
   ```
3. O relatório final será gerado na pasta `output/`.

