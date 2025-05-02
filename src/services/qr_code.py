import qrcode
from qrcode.image.svg import SvgPathFillImage

class QrCodeService:
    def __init__(self):
        """
        Инициализация сервиса QR-кодов.
        """
        pass

    def GenerateQrCode(self, data:str) -> str:
        """
        Генерирует QR-код на основе переданных данных.

        :param data: Данные для кодирования в QR-код.
        :return: Путь к сгенерированному QR-коду.
        """
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        return qr.make_image(fill_color="black", back_color="white")
    
    def GenerateQrCodeSvg(self, data:str, size:int=200) -> str:
        """
        Генерирует QR-код в формате SVG на основе переданных данных (фиксированные размеры и стандартные атрибуты).

        :param data: Данные для кодирования в QR-код.
        :return: Строка с SVG-кодом QR-кода.
        """
        qr = qrcode.QRCode(
            image_factory=SvgPathFillImage,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        svg_string = img.to_string().decode('utf-8').replace('width="37mm"', f'width="{size}px"').replace('height="37mm"', f'height="{size}px"')
        return svg_string

qrcode_service = QrCodeService()