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

if __name__ == "__main__":
    # Передаем client_token из конфигурации
    qrcode_service = QrCodeService()
    qrcode_img = qrcode_service.GenerateQrCode("https://example.com")
    print(type(qrcode_img))  # qrcode.image.pil.PilImage
    qrcode_img.save("qrcode.png")