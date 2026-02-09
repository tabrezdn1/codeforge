"""Document processing tools for CodeForge."""

from google.cloud import storage


def read_document_from_gcs(uri: str) -> str:
    """
    Reads a document from Google Cloud Storage and returns its text content.

    Args:
        uri: GCS URI in format gs://bucket/path/to/file

    Returns:
        The document content as a string.
    """
    if not uri.startswith("gs://"):
        return f"Error: Invalid GCS URI format. Expected gs://bucket/path, got: {uri}"

    try:
        parts = uri.replace("gs://", "").split("/", 1)
        bucket_name = parts[0]
        blob_path = parts[1] if len(parts) > 1 else ""

        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_path)

        content = blob.download_as_bytes()

        if uri.endswith(".pdf"):
            try:
                from pypdf import PdfReader
                from io import BytesIO

                reader = PdfReader(BytesIO(content))
                pages = []
                for i, page in enumerate(reader.pages):
                    text = page.extract_text()
                    pages.append(f"[Page {i + 1}]\n{text}")
                return "\n\n".join(pages)
            except ImportError:
                return "Error: pypdf not installed. Run: pip install pypdf"
        else:
            return content.decode("utf-8")

    except Exception as e:
        return f"Error reading document from GCS: {e}"
