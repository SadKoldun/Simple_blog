from typing import List
from sqlalchemy import create_engine
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


db = SQLAlchemy()


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title = mapped_column(String(250), unique=True, nullable=False)
    subtitle = mapped_column(String(250), nullable=False)
    date = mapped_column(String(250), nullable=False)
    body = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship(back_populates="post")
    img_url = mapped_column(String(250), nullable=False)
    comments_from_post: Mapped[List["Comment"]] = relationship(back_populates="post_with_comment", cascade="all, delete")


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email = mapped_column(String(250), unique=True, nullable=False)
    password = mapped_column(String(250), nullable=False)
    name = mapped_column(String(250), nullable=False)
    post: Mapped[List["BlogPost"]] = relationship(back_populates="author")
    user_comments: Mapped[List['Comment']] = relationship(back_populates="comment_author")


class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    text = mapped_column(String(250), unique=True, nullable=False)
    comment_author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    comment_author: Mapped["User"] = relationship(back_populates="user_comments")
    post_with_comment_id: Mapped[int] = mapped_column(ForeignKey("blog_posts.id"))
    post_with_comment: Mapped["BlogPost"] = relationship(back_populates="comments_from_post")
