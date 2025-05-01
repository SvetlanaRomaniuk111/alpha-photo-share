from sqlalchemy.ext.asyncio import AsyncSession
from src.models.transformed_image import TransformedImage

async def save_transformed_image(user_id: int, original_url: str, transformed_url: str, qr_code_url: str, db: AsyncSession):
    new_entry = TransformedImage(
        user_id=user_id,
        original_url=original_url,
        transformed_url=transformed_url,
        qr_code_url=qr_code_url
    )
    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)
    return new_entry