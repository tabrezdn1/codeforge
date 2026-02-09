"""Rendering and diagram tools for CodeForge."""

import os
import requests

from google.cloud import storage


def generate_diagram_from_mermaid(mermaid_syntax: str, file_name: str = "architecture") -> str:
    """
    Renders Mermaid diagram syntax into a PNG image using the Kroki API,
    uploads it to Google Cloud Storage, and returns the public URL.

    Args:
        mermaid_syntax: The Mermaid syntax string to render.
        file_name: Base name for the output file.

    Returns:
        The public URL of the generated diagram image, or an error message.
    """
    bucket_name = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
    if not bucket_name:
        return "Error: GOOGLE_CLOUD_STORAGE_BUCKET environment variable not set."

    # Clean up the mermaid syntax
    processed = mermaid_syntax.replace("\\n", "\n").replace('\\"', '"')

    try:
        # Use Kroki API for rendering (no browser dependency needed for POC)
        response = requests.post(
            "https://kroki.io/mermaid/png",
            data=processed.encode("utf-8"),
            headers={"Content-Type": "text/plain"},
            timeout=30,
        )

        if response.status_code != 200:
            return f"Error: Kroki API returned status {response.status_code}: {response.text[:200]}"

        png_bytes = response.content

        # Upload to GCS
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob_name = f"diagrams/{file_name}.png"
        blob = bucket.blob(blob_name)
        blob.upload_from_string(png_bytes, content_type="image/png")
        blob.make_public()

        print(f"INFO: Diagram uploaded to gs://{bucket_name}/{blob_name}")
        return blob.public_url

    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to Kroki API. Check internet connection."
    except Exception as e:
        return f"Error generating diagram: {e}"
