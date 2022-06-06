from models.author import Author
from utils.const import ISBN_DESCRIPTION
from typing import Optional, List
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship


# None is the default value
class Book(SQLModel, table=True):
    isbn: Optional[int] = Field(default=None, primary_key=True)#, description=ISBN_DESCRIPTION)
    name: str
    year: int = Field(None, gt=1900, lt=2050)
    author_id: Optional[int] = Field(default=None, foreign_key="author.id")
    author: Optional[Author] = Relationship(back_populates="books")



sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    with Session(engine) as session:
        author_kerouac = Author(name="Kerouac")
        author_rowling = Author(name="Rowling")
        book_ontheroad = Book(name="On the Road", year=1992, author=author_kerouac)
        book_potter = Book(name="Harry Potter", year=2001, author=author_rowling)
        session.add(book_ontheroad)
        session.add(book_potter)
        session.commit()
        session.refresh(book_ontheroad)
        session.refresh(book_potter)
        print("Created book:", book_ontheroad)
        print("Created book:", book_potter)

        book_ontheroad.author = author_kerouac
        book_potter.author = author_rowling
        session.add(book_ontheroad)
        session.add(book_potter)
        session.commit()
        session.refresh(book_ontheroad)
        session.refresh(book_potter)
        print("Updated book:", book_ontheroad)
        print("Updated book:", book_potter)
        author_kerouac.books.append(book_ontheroad)
        author_rowling.books.append(book_potter)
        session.add(author_kerouac)
        session.add(author_rowling)
        session.commit()
        session.refresh(book_ontheroad)
        session.refresh(book_potter)
        print("Author", author_kerouac, author_rowling)
        print("new books:", book_ontheroad, book_potter)

def select_book_with_author(book_name):
    with Session(engine) as session:
        statement = select(Book).where(Book.name == book_name)
        result = session.exec(statement)
        book_result = result.one()
        # Code from the previous example omitted 👈
        print("Book with author", book_result.author)
        print("Also printing full book object : ", book_result)

def select_author_with_books(author_name):
    with Session(engine) as session:
        statement = select(Author).where(Author.name == author_name)
        result = session.exec(statement)
        author_results = result.one()

        print("Author Books:", author_results.books)

'''
def main():
    create_db_and_tables()
    create_heroes()
    select_book_with_author("On the Road")
    select_book_with_author("Harry Potter")
    select_author_with_books("Kerouac")
    select_author_with_books("Rowling")

if __name__ == "__main__":
    main()
'''