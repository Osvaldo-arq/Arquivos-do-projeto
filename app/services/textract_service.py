# textract_service.py
import boto3
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

textract_client = boto3.client("textract", region_name="us-east-1")

class TextractService:
    def process_invoice(self, bucket_name: str, file_key: str) -> dict:
        """
        Usa detect_document_text para extrair as linhas do documento.
        Retorna {"status": "success", "text": [...] } ou {"status": "error", "message": "..."}.
        """
        try:
            logger.info(f"Chamando Textract para Bucket={bucket_name}, Key={file_key}")
            response = textract_client.detect_document_text(
                Document={"S3Object": {"Bucket": bucket_name, "Name": file_key}}
            )
            extracted_text = [
                block["Text"] for block in response.get("Blocks", [])
                if block["BlockType"] == "LINE"
            ]
            logger.info(f"Texto extraído: {extracted_text[:5]}...")
            return {"status": "success", "text": extracted_text}
        except Exception as e:
            logger.error(f"Erro no Textract: {str(e)}")
            return {"status": "error", "message": str(e)}
