import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential


def extract_text_from_image(image_path=None):
    """
    Extract text from an image using Azure Computer Vision OCR.

    Args:
        image_path (str, optional): Path to local image file

    Returns:
        dict: Contains 'text' (full extracted text) and 'lines' (list of text lines)

    Raises:
        Exception: If OCR operation fails
    """
    # Get credentials
    endpoint = os.getenv("ENDPOINT")
    key = os.getenv("AZURE_KEY")

    # Create client
    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    # Perform OCR
    try:
        # Analyze from local file
        with open(image_path, 'rb') as f:
            image_data = f.read()
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
        image_path="TEST.png"
    )
    print("Extracted text:")
    print(result['text'])
