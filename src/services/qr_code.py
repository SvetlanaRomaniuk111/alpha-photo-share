import qrcode
from qrcode.image.svg import SvgPathFillImage
from qrcode.image.pil import PilImage

class QrCodeService:
    def __init__(self):
        """
        Инициализация сервиса QR-кодов.
        """
        pass

    def generatePilImage(self, data:str) -> PilImage:
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
    
    def generateSvg(self, data:str, size:int=200) -> str:
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
    
    async def generatePilImageAsync(self, data:str) -> PilImage:
        """
        Асинхронно генерирует QR-код на основе переданных данных.

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
    
    async def generateSvgAsync(self, data:str, size:int=200) -> str:
        """
        Асинхронно генерирует QR-код в формате SVG на основе переданных данных (фиксированные размеры и стандартные атрибуты).

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