from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import json
from app.services.s3_service import S3Service
from app.services.textract_service import TextractService
from app.services.nlp_service import process_text

router = APIRouter()
s3_service = S3Service()
textract_service = TextractService()

@router.post("/api/v1/invoice")
async def upload_invoice(file: UploadFile = File(...)):
    try:
        # Mantém o nome original do arquivo
        file_name = file.filename

        # Lê os bytes do arquivo
        file_bytes = await file.read()

        # 1) Upload para S3 (bucket de entrada)
        s3_key = s3_service.upload_file(file_bytes, file_name)

        # 2) Processar com Textract (arquivo no S3)
        textract_result = textract_service.process_invoice(
            s3_service.input_bucket, s3_key
        )
        if textract_result.get("status") == "error":
            raise HTTPException(
                status_code=500, detail=f"Erro no Textract: {textract_result['message']}"
            )

        # 3) NLP com spaCy
        # Concatena as linhas extraídas do Textract
        raw_text = " ".join(textract_result.get("text", []))
        structured_data = process_text(raw_text)

        # 4) Salva o resultado JSON no bucket de saída
        result_filename = f"{file_name}.json"
        result_data = json.dumps(structured_data)
        output_key = s3_service.save_result(result_data, result_filename)

        return {
            "message": "Processamento concluído",
            "original_s3_url": f"s3://{s3_service.input_bucket}/{s3_key}",
            "result_s3_url": f"s3://{s3_service.output_bucket}/{output_key}",
            "extracted_data": structured_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento: {str(e)}")


@router.get("/api/v1/invoice/{file_name}")
def get_processed_invoice(file_name: str):
    try:
        # Nome do arquivo esperado no bucket de saída
        result_filename = f"{file_name}"
        
        # Busca o conteúdo do arquivo JSON no S3
        result_data = s3_service.get_result(result_filename)
        
        if not result_data:
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")
        
        return json.loads(result_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao recuperar o arquivo: {str(e)}")
