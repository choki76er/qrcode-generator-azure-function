import io
import logging

import azure.functions as func
import qrcode


# MIT License - https://opensource.org/licenses/MIT

# For my use, I want to restrict which URLs I allow generation for since I am running without API access.
# You can add more prefixes to this list if you want to allow QR generation for other sites.

ALLOWED_PREFIXES = ["https://google.com/","https://microsoft.com/"]


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    This function is the main entry point for the Azure Function.
    It will be called when the function is triggered.


    Args:
        req (func.HttpRequest): The HTTP request object.

    Returns:
        func.HttpResponse: The HTTP response object - either a plaintext error or a PNG encoded QR code image.
    """

    string_to_convert = req.params.get("data")
    
    if not string_to_convert:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            try:
                string_to_convert = req_body["data"]
            except KeyError:
                pass

    if string_to_convert is None:
        return func.HttpResponse(
            "Please pass a value for data in the query string or in request body.", status_code=400
        )
    else:
            # If you don't care about validating the URL, you can remove this check.
        if allowed_prefix(string_to_convert):
            # TODO if you wish: Expose box size and border to the API.
            box_size = 5
            border = 2
            img_data = make_qr(string_to_convert, box_size, border)
            return func.HttpResponse(img_data, mimetype="image/png", status_code=200)
        else:
            logging.warn(
                f"Request fails to meet prefix criteria - unable to create QR code for {string_to_convert}."
            )
            return func.HttpResponse(f"{string_to_convert} not in allowed list of prefixes", status_code=401)


def make_qr(data_to_encode, box_size, border):
    """
    This function will create a QR code for the given data

    If the box size passed in is too small, it will auto-adjust to the smallest size that will fit the data.

    Args:
        data_to_encode (string): The string to generate a QR code for.
        box_size (int): The QR code's box size.
        border (int): The QR code border size.

    Returns:
        bytes: The PNG encoded QR code image as bytes.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data_to_encode)
    # fit=True will override the box size if the data is too large for the given box size.
    qr.make(fit=True)
    img = qr.make_image()
    img_buf = io.BytesIO()
    img.save(img_buf)
    img_buf.seek(0)
    return img_buf.getvalue()


def allowed_prefix(data):
    """
    This checks to see if the data matches any of the allowed prefixes.

    Args:
        data (string): The string to check.

    Returns:
        boolean: True if the URL is valid, False if invalid.
    """

    for prefix in ALLOWED_PREFIXES:
        if data.startswith(prefix):
            return True
    return False
