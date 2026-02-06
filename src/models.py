from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

# -------------------------
# TABLA INTERMEDIA FOLLOWERS
# -------------------------
follower_table = Table(
    "followers",
    db.Model.metadata,
    Column("following_id", ForeignKey("user.id"), primary_key=True),
    Column("follower_id", ForeignKey("user.id"), primary_key=True)
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    

    comentarios: Mapped[list["Comment"]] = relationship(back_populates=("user"))


    post: Mapped[list["Post"]] = relationship(back_populates=("user"))

    followers: Mapped[list["User"]] = relationship(
        "User",
        secondary=follower_table,
        primaryjoin="follower_table.following_id == User.id",
        secondaryjoin="follower_table.follower_id == User.id",
        back_populates="following"
    )

    following: Mapped[list["User"]] = relationship(
        "User",
        secondary=follower_table,
        primaryjoin="follower_table.follower_id == User.id",
        secondaryjoin="follower_table.following_id == User.id",
        back_populates="followers"

    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(
        back_populates="post"
    )

    comentarios: Mapped[list["Comment"]] = relationship(
        back_populates="post"
    )

    medias: Mapped[list["Media"]] = relationship(
        back_populates="post"
    )

    def serialize(self):
        return {
            "id": self.id
        }


class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(120), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship(
        back_populates="comentarios"
    )

    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(
        back_populates="comentarios"
    )

    def serialize(self):
        return {
            "id": self.id,
            "comment": self.comment_text
        }


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(
        back_populates="medias"
    )

    def serialize(self):
        return {
            "id": self.id,
            "url": self.url
        }


