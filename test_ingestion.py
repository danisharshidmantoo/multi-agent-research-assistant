from rag.pipeline import IngestionPipeline


pipeline = IngestionPipeline()

result = pipeline.ingest()

print(result)