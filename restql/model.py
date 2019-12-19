from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
            self.name, self.fullname, self.nickname)


from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address


User.addresses = relationship(
    "Address", order_by=Address.id, back_populates="user")

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('sqlite:///test.db', echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    entry1 = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
    entry1.addresses = [Address(email_address='ed@gmail.com')]

    entry2 = User(name='wendy', fullname='Wendy Williams', nickname='windy')
    entry2.addresses = [Address(email_address='wendy@gmail.com')]

    entry3 = User(name='mary', fullname='Mary Contrary', nickname='mary')
    entry3.addresses = [Address(email_address='mary@gmail.com')]

    entry4 = User(name='fred', fullname='Fred Flintstone', nickname='freddy')
    entry4.addresses = [Address(email_address='fred@gmail.com')]

    session.add(entry1)
    session.add(entry2)
    session.add(entry3)
    session.add(entry4)

    # session.add_all([entry1, entry2, entry3, entry4])

    print(session.query(User).all())
    session.commit()

