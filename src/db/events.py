from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from src.models import PostTag

@event.listens_for(Session, "before_flush")
def validate_max_five_tags(session, flush_context, instances):
    for obj in session.new:
        if isinstance(obj, PostTag):
            #TODO: create repo func to get all tags for post(вынести постайди в переменную)
            stmt = select(PostTag).where(PostTag.post_id == obj.post_id)
            existing_tags = session.execute(stmt).scalars().all()
            if len(existing_tags) >= 5:
                raise IntegrityError(None, None, "Cannot add more than 5 tags to a post.")