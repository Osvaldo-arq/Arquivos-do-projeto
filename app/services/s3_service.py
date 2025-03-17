import os
import boto3
import logging
import mimetypes
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

s3_client = boto3.client("s3")

class S3Service:
    def __init__(self):
        # Carrega buckets do arquivo .env ou variáveis do ambiente
        self.input_bucket = os.getenv("INPUT_BUCKET")
        self.output_bucket = os.getenv("OUTPUT_BUCKET")
        if not self.input_bucket or not self.output_bucket:
            raise ValueError("Variáveis INPUT_BUCKET e OUTPUT_BUCKET não definidas.")

    def upload_file(self, file_content: bytes, filename: str) -> str:
        s3_key = f"notas/{filename}"
        
        # Detecta automaticamente o tipo de arquivo
        content_type, _ = mimetypes.guess_type(filename)
        if content_type is None:
            content_type = "application/octet-stream"  

        s3_client.put_object(
            Bucket=self.input_bucket,
            Key=s3_key,
            Body=file_content,
            ContentType=content_type  
        )
        logger.info(f"Arquivo {filename} enviado para {self.input_bucket}/{s3_key} com ContentType={content_type}")
        return s3_key

    def save_result(self, result_data: str, result_filename: str) -> str:
        s3_key = f"processed/{result_filename}"
        s3_client.put_object(
            Bucket=self.output_bucket,
            Key=s3_key,
            Body=result_data,
            ContentType="application/json"
        )
        logger.info(f"Resultado salvo em {self.output_bucket}/{s3_key}")
        return s3_key
