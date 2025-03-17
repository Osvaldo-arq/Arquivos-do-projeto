import re
import spacy

nlp = spacy.blank("pt")

def process_text(text_data):
    extracted_data = {
        "nome_emissor": None,
        "CNPJ_emissor": None,
        "endereco_emissor": None,
        "CNPJ_CPF_consumidor": None,
        "data_emissao": None,
        "numero_nota_fiscal": None,
        "serie_nota_fiscal": None,
        "valor_total": None,
        "forma_pgto": None
    }

    # Processamento com NLP
    doc = nlp(text_data)
    for ent in doc.ents:
        if ent.label_ == "CNPJ" and not extracted_data["CNPJ_emissor"]:
            extracted_data["CNPJ_emissor"] = ent.text
        elif ent.label_ == "CPF" and not extracted_data["CNPJ_CPF_consumidor"]:
            extracted_data["CNPJ_CPF_consumidor"] = ent.text
        elif ent.label_ == "DATE" and not extracted_data["data_emissao"]:
            extracted_data["data_emissao"] = ent.text
        elif ent.label_ == "NOTAFISCAL" and not extracted_data["numero_nota_fiscal"]:
            extracted_data["numero_nota_fiscal"] = ent.text
        elif ent.label_ == "VALOR" and not extracted_data["valor_total"]:
            extracted_data["valor_total"] = ent.text
        elif ent.label_ == "PAGAMENTO" and not extracted_data["forma_pgto"]:
            extracted_data["forma_pgto"] = ent.text

    # Regex Patterns
    patterns = {
        "cnpj": r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}",
        "cpf": r"\d{3}\.\d{3}\.\d{3}-\d{2}",
        "data": r"\d{2}/\d{2}/\d{4}",
        "serie_nota_fiscal": r"SAT No\. (\d+)|Série:\s*(\d+)",
        "forma_pgto": r"(?i)(dinheiro|pix|débito|crédito|cheque|DEBITO|CREDITO|DÉBITO|CRÉDITO|CARTAO DE CREDITO|CARTAO DE DEBITO)",
        "valor_total": r'R\$\s*(\d+[,.]\d+)',
        "nome_emissor": r"^(.*?)(?=\s*CNPJ|\s*End\.|\s*Rua|\s*Avenida|\s*Av\.|\s*CEP|\s*LTDA|\s*RUA|\s*ALAMEDA)",
        "endereco_emissor": r"(?:End\.:\s*|Rua\s*|Avenida\s*|Av\.|AVENIDA\s*|Rodovia\s*|BR|RODOVIA|ALAMEDA)[\s\S]*?(?=\s*CEP \d{5}-\d{3}|\s*CNPJ|\s*TEL|\s*CEP)",
        "numero_nota_fiscal": r"Extrato No\s*(\d+)",
        "CNPJ_emissor" : r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text_data, re.MULTILINE | re.DOTALL)
        if match:
            if key == "cnpj" and not extracted_data["CNPJ_emissor"]:
                extracted_data["CNPJ_emissor"] = match.group(0)
            elif key == "cpf" and not extracted_data["CNPJ_CPF_consumidor"]:
                extracted_data["CNPJ_CPF_consumidor"] = match.group()
            elif key == "data" and not extracted_data["data_emissao"]:
                extracted_data["data_emissao"] = match.group()
            elif key == "numero_nota_fiscal" and not extracted_data["numero_nota_fiscal"]:
                extracted_data["numero_nota_fiscal"] = match.group(1)
            elif key == "serie_nota_fiscal" and not extracted_data["serie_nota_fiscal"]:
                extracted_data["serie_nota_fiscal"] = match.group(1) or match.group(2)
            elif key == "forma_pgto" and not extracted_data["forma_pgto"]:
                extracted_data["forma_pgto"] = match.group(1).capitalize()
            elif key == "valor_total" and not extracted_data["valor_total"]:
                extracted_data["valor_total"] = "R$ " + match.group(1)
            elif key == "nome_emissor" and not extracted_data["nome_emissor"]:
                extracted_data["nome_emissor"] = match.group(1).strip()
            elif key == "endereco_emissor" and not extracted_data["endereco_emissor"]:
                extracted_data["endereco_emissor"] = match.group(0).strip()

    return extracted_data
