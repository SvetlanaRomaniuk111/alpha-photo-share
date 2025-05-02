from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from src.models.transformed_images import TransformedImage

from uuid import UUID

async def get_transformed_images_for_user(user_id: int, db: AsyncSession):
    """
    Retrieve all transformed images for a specific user.

    This function queries the database to find all transformed images that belong to a given user.

    Args:
        user_id (int): The ID of the user whose transformed images should be retrieved.
        db (AsyncSession): The asynchronous database session.

    Returns:
        list[TransformedImage]: A list of transformed images belonging to the user.
    """
    stmt = select(TransformedImage).options(joinedload(TransformedImage.user)).filter(
        TransformedImage.user_id == user_id
    )
    result = await db.execute(stmt)

    return result.scalars().all()


async def save_transformed_image(
    user_id: UUID, original_url: str, transformed_url: str, db: AsyncSession
):
    """
    Save a transformed image record to the database.

    This function creates a new entry in the transformed_images table and commits it.

    Args:
        user_id (UUID): The UUID of the user associated with the transformed image.
        original_url (str): URL of the original image.
        transformed_url (str): URL of the transformed image.
        db (AsyncSession): The asynchronous database session.

    Returns:
        TransformedImage: The newly saved transformed image record.
    """
    new_entry = TransformedImage(
        user_id=user_id,
        original_url=original_url,
        transformed_url=transformed_url,
    )
    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)
    return new_entry
