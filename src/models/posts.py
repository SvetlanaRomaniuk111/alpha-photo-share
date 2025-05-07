
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import String, Integer, DateTime, ForeignKey, func, text
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.db.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.transformed_images import TransformedImage
    from src.models.users import User


class Post(Base):
    __tablename__ = "posts"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship("User", back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post")
    tags: Mapped[list["PostTag"]] = relationship(
        "PostTag",
        back_populates="post",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    ratings: Mapped[list["PostRating"]] = relationship(
        "PostRating", back_populates="post"
    )
    transformed_images: Mapped[list["TransformedImage"]] = relationship(
        "TransformedImage", back_populates="post", lazy="select"
    )

class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    post_id: Mapped[UUID] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))
    message: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
    
    post: Mapped["Post"] = relationship("Post", back_populates="comments")


class PostRating(Base):
    __tablename__ = "post_ratings"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    post_id: Mapped[UUID] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))
    rating: Mapped[int] = mapped_column(Integer, nullable=False)

    post: Mapped["Post"] = relationship("Post", back_populates="ratings")


class PostTag(Base):
    __tablename__ = "post_tags"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    post_id: Mapped[UUID] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))
    tag_id: Mapped[str] = mapped_column(ForeignKey("tags.id", ondelete="CASCADE"))

    post: Mapped["Post"] = relationship("Post", back_populates="tags")
    tag: Mapped["Tag"] = relationship("Tag", back_populates="post_tags")


class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    post_tags: Mapped[list["PostTag"]] = relationship("PostTag", back_populates="tag")
