from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

class ImageProcessor:
    """Клас для обробки зображень через Cloudinary.

    Цей клас містить методи для виконання основних операцій зображеннями, таких як завантаження, 
    зміна розміру, накладання фільтрів, зміна формату та оптимізація.
    """

    @staticmethod
    def upload_image(file_path: str) -> str:
        """
        Завантажує зображення на Cloudinary.

        Args:
            file_path (str): Шлях до файлу зображення, яке потрібно завантажити.

        Returns:
            str: URL завантаженого зображення.
        """
        result = upload(file_path)
        return result["url"]

    @staticmethod
    def resize_image(image_url: str, width: int, height: int) -> str:
        """
        Змінює розмір зображення за заданими параметрами.

        Args:
            image_url (str): URL оригінального зображення.
            width (int): Бажана ширина зображення.
            height (int): Бажана висота зображення.

        Returns:
            str: URL зміненого зображення.
        """
        url, _ = cloudinary_url(
            image_url, width=width, height=height, crop="fill", fetch_format="auto", quality="auto"
        )
        return url

    @staticmethod
    def apply_filter(image_url: str, effect: str) -> str:
        """
        Накладає фільтр або ефект на зображення.

        Args:
            image_url (str): URL оригінального зображення.
            effect (str): Назва ефекту (наприклад, "grayscale", "sepia").

        Returns:
            str: URL зображення з накладеним ефектом.
        """
        url, _ = cloudinary_url(image_url, transformation=[{"effect": effect}])
        return url

    @staticmethod
    def optimize_image(image_url: str) -> str:
        """
        Оптимізує зображення, зменшуючи його вагу без втрати якості.

        Args:
            image_url (str): URL оригінального зображення.

        Returns:
            str: URL оптимізованого зображення.
        """
        url, _ = cloudinary_url(
            image_url, quality="auto", fetch_format="auto", version="new_version"
        )
        return url
