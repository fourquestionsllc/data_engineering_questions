To query a PostgreSQL database using **SQLAlchemy** in Python, you can use either:

1. **SQLAlchemy Core** (low-level, SQL-like)
2. **SQLAlchemy ORM** (object-relational mapping)

Here’s how to do both with PostgreSQL.

---

## ✅ Step-by-Step with SQLAlchemy ORM (Recommended for most cases)

### 1. **Install Requirements**

```bash
pip install sqlalchemy psycopg2-binary
```

---

### 2. **Define the Connection and ORM Models**

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# PostgreSQL connection URL
DATABASE_URL = "postgresql+psycopg2://username:password@localhost:5432/your_db_name"

# Create engine
engine = create_engine(DATABASE_URL)

# Define base model
Base = declarative_base()

# Define a table as a Python class
class User(Base):
    __tablename__ = 'users'  # your actual table name
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

# Create session
Session = sessionmaker(bind=engine)
session = Session()
```

---

### 3. **Query the Database**

```python
# Query all users
users = session.query(User).all()

# Print results
for user in users:
    print(user.id, user.name, user.email)
```

---

### 4. **Filter, Insert, Update, Delete Examples**

#### Filter:

```python
user = session.query(User).filter_by(name="Alice").first()
```

#### Insert:

```python
new_user = User(name="Bob", email="bob@example.com")
session.add(new_user)
session.commit()
```

#### Update:

```python
user.name = "Robert"
session.commit()
```

#### Delete:

```python
session.delete(user)
session.commit()
```

---

## 🧠 Tip: Using SQLAlchemy Core (No ORM)

If you don’t want to use the ORM, use raw SQL-like syntax:

```python
from sqlalchemy import create_engine, text

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM users"))
    for row in result:
        print(row)
```

---

## ⚡ Optional: Use with Async SQLAlchemy

Want to use SQLAlchemy with async + PostgreSQL (e.g., with FastAPI)? Let me know and I can show you how to use `asyncpg` with `SQLAlchemy 2.0` using `async_engine`.

---
