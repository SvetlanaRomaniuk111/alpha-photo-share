import qrcode
from qrcode.image.svg import SvgPathFillImage
from qrcode.image.pil import PilImage
import asyncio
from PIL import Image
class QrCodeService:
    async def generatePilImageAsync(self, data: str, size: int = 200) -> Image:
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        # Масштабируем изображение до нужного размера
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        return img

    def generatePilImage(self, data: str, size: int = 200) -> Image:
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        # Масштабируем изображение до нужного размера
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        return img
    
    async def generateSvgAsync(self, data:str, size:int=200) -> str:
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
    
    def generateSvg(self, data:str, size:int=200) -> str:
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