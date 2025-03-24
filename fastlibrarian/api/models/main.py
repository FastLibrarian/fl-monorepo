from sqlalchemy import (
    Column,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)


class Issue(Base):
    __tablename__ = "issues"

    Title = Column(String, ForeignKey("magazines.Title", ondelete="CASCADE"))
    IssueID = Column(String, primary_key=True, unique=True)


class Download(Base):
    __tablename__ = "downloads"

    Count = Column(Integer, default=0)
    Provider = Column(String, primary_key=True)


class SeriesAuthor(Base):
    __tablename__ = "seriesauthors"

    SeriesID = Column(String, primary_key=True)
    AuthorID = Column(
        String, ForeignKey("authors.AuthorID", ondelete="CASCADE"), primary_key=True
    )


class Member(Base):
    __tablename__ = "member"

    __table_args__ = (
        UniqueConstraint("SeriesID", "BookID"),
        Index("unq", "SeriesID", "BookID"),
    )


class Subscriber(Base):
    __tablename__ = "subscribers"

    UserID = Column(
        String, ForeignKey("users.UserID", ondelete="CASCADE"), primary_key=True
    )
    Type = Column(String, primary_key=True)
    WantID = Column(Text)  # Changed to Text to match schema
