from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.core import log

general_check_router = APIRouter(prefix='/general', tags=['general'])

@general_check_router.get("/health_checker")
async def health_checker(db: AsyncSession = Depends(get_db)):
    try:
        # Make request
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        log.debug(result)
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )

        return {"message": "Database is connected and healthy", "result": result[0]}

    except Exception as e:
        log.error(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")