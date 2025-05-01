import qrcode

class QrCodeService:
    def GenerateQrCode(self, data: str) -> str:
        """
        Генерирует QR-код на основе переданных данных.

        :param data: Данные для кодирования в QR-код.
        :return: Путь к сгенерированному QR-коду.
        """
        qrcode_img = qrcode.make(data)
        return qrcode_img

qrcode_service = QrCodeService()