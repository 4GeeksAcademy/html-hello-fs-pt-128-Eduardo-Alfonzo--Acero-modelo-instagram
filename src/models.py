from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey,Column,Table
from sqlalchemy.orm import Mapped, mapped_column,relationship

db = SQLAlchemy()

follower_table = Table(
    "followers",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("follower_id", ForeignKey("follower.id"), primary_key=True)
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    comentarios: Mapped[list["Comment"]]= relationship()
    post:Mapped [list["Post"]]= relationship()
    follower: Mapped[list["Follower"]]=relationship(
        "Follower",
        secondary=follower_table,
        back_populates= "followers"
    )



    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Post (db.Model):
    id:Mapped[int]=mapped_column(primary_key=True)
    comentarios:Mapped [list["Comment"]]= relationship()
    medias: Mapped[list["Media"]] = relationship()
    user_id: Mapped [int]= mapped_column(ForeignKey("user.id"))
    user: Mapped [User] = relationship(back_populates="post")




    
    def serialize(self):
        return{
            "id":self.id,
        }
    


class Comment (db.Model):
     id: Mapped[int] = mapped_column(primary_key=True)
     comment_text: Mapped[str] = mapped_column(String(120),)
     user_id: Mapped [int]= mapped_column(ForeignKey("user.id"))
     user: Mapped [User] = relationship(back_populates="comentarios") 
     post_id: Mapped[str]= mapped_column(ForeignKey("post.id"))
     post: Mapped[Post] = relationship (back_populates="comentarios")



     def serializa(self):
         return{
             "id":self.id,
             "comment":self.comment_text
         }
     
class Media (db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(120), unique=True,)
    post_id: Mapped[int]= mapped_column(ForeignKey("post.id"))
    post: Mapped[Post] = relationship (back_populates="medias")


    def serialize(self):
        return{
            "id":self.id,
            "url":self.url
            
        }

class Follower (db.Model): 
    id: Mapped[int] = mapped_column(primary_key=True)
    followers:Mapped[list[User]]=relationship(
        "User",
        secondary=follower_table,
        back_populates="follower"
        
    )




