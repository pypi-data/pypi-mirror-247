from PIL import Image
import base64
from io import BytesIO

def image_to_base64(image: Image.Image) -> str:
    """
    Convert an image to base64 string.

    Parameters:
        image (Image.Image): The image to convert.

    Returns:
        str: The base64 string of the image.
    """
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def base64_to_image(base64_string: str) -> Image.Image:
    """
    Convert a base64 string to an image.

    Parameters:
        base64_string (str): The base64 string to convert.

    Returns:
        Image.Image: The image created from the base64 string.
    """
    img_data = base64.b64decode(base64_string)
    img = Image.open(BytesIO(img_data))
    return img