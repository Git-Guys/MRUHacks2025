import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from io import BytesIO
from PIL import Image


def extract_text_from_image(image_obj=None):
    """
    Extract text from an image using Azure Computer Vision OCR.

    Args:
        image_obj (Image, optional): Image object

    Returns:
        dict: Contains 'text' (full extracted text) and 'lines' (list of text lines)

    Raises:
        Exception: If OCR operation fails
    """
    # Get credentials
    endpoint = os.getenv("AZURE_ENDPOINT")
    key = os.getenv("AZURE_KEY")

    # Create client
    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    # Perform OCR
    try:
        # Convert PIL Image to bytes
        buf = BytesIO()
        image_obj.save(buf, format="PNG") # write the image into memory
        image_data = buf.getvalue() # get raw bytes

        result = client.analyze(
            image_data=image_data,
            visual_features=[VisualFeatures.READ]
        )

        # Extract text results
        lines = []
        full_text = []

        if result.read and result.read.blocks:
            for block in result.read.blocks:
                for line in block.lines:
                    line_text = line.text
                    lines.append({
                        'text': line_text,
                        'bounding_box': line.bounding_polygon
                    })
                    full_text.append(line_text)

        return {
            'text': '\n'.join(full_text),
            'lines': lines
        }

    except Exception as e:
        raise Exception(f"OCR failed: {str(e)}")


if __name__ == "__main__":
    result = extract_text_from_image(
        image_path="MRUHacks2025/B Sum B.pdf"
    )
    print("Extracted text:")
    print(result['text'])
