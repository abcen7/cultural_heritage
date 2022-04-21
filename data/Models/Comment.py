from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, orm
from Classes.SqlAlchemyDatabase import SqlAlchemyBase


class Comment(SqlAlchemyBase):
    __tablename__ = "comments"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    belongs_to_object = Column(Integer, ForeignKey("objects.id"))
    created_by = Column(ForeignKey("users.id"), nullable=False)
    object = orm.relationship("Object", back_populates="comment")
    user = orm.relation("User")

    def __repr__(self):
        return '<Comment {}>'.format(self.text)
