# QR Code Generator Azure Function

QR Code Generator Azure Function does what it says on the label - takes data and uses the qrcode Python library to convert to a PNG image.

## Installation

You can use the Deployment Zip Push method if you wish - download this repository as a Zip and then upload using Azure CLI.

```bash
az functionapp deployment source config-zip -g <resource_group> -n \
QRCodeGenerator --src QRCodeGenerator.zip
```

## Usage

Visit your Function URL and append ?data= to return a QR code.

You can also do a POST with a JSON payload of:
### POST Method
``POST http://<your-azure-function-address>/api/QRCodeGenerator``

``
{"data":"https://google.com/"}
``
### GET Method
```
http://<your-azure-function-address>/api/QRCodeGenerator?data=https://google.com/
```

## Contributing
Pull requests are welcome - this does what I need and should hopefully be clear enough to help you tailor it as required.

## License
[MIT](https://choosealicense.com/licenses/mit/)