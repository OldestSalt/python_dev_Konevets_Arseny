from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship


Base = declarative_base()

class Posts(Base):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    header: Mapped[str] = mapped_column(String(100))
    text: Mapped[str] = mapped_column(String(1000))
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("author.id"))
    author: Mapped["Authors"] = relationship("Authors", back_populates="posts")
    blog_id: Mapped[int] = mapped_column(Integer, ForeignKey("blog.id"))
    blog: Mapped["Blogs"] = relationship("Blogs", back_populates="posts")
    comments: Mapped[list["Comments"]] = relationship("Comments", back_populates="post", cascade="all, delete-orphan")


class Authors(Base):
    __tablename__ = "author"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    blogs: Mapped[list["Blogs"]] = relationship("Blogs", back_populates="owner", cascade="all, delete-orphan")
    posts: Mapped[list["Posts"]] = relationship("Posts", back_populates="author", cascade="all, delete-orphan")
    comments: Mapped[list["Comments"]] = relationship("Comments", back_populates="author", cascade="all, delete-orphan")
    email: Mapped[str] = mapped_column(String(100))
    login: Mapped[str] = mapped_column(String(100))


class Blogs(Base):
    __tablename__ = "blog"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    posts: Mapped[list["Posts"]] = relationship("Posts", back_populates="blog", cascade="all, delete-orphan")
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("author.id"))
    owner: Mapped["Authors"] = relationship("Authors", back_populates="blogs")
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1000))


class Comments(Base):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("author.id"))
    author: Mapped["Authors"] = relationship("Authors", back_populates="comments")
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("post.id"))
    post: Mapped["Posts"] = relationship("Posts", back_populates="comments")
    text: Mapped[str] = mapped_column(String(1000))