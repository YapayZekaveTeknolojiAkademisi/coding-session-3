from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite veritabanı dosyasının yolu. Yerel geliştirme için test.db dosyası kullanılır.
DATABASE_URL = "sqlite:///./test.db"

# SQLAlchemy motorunu (engine) oluşturuyoruz. 
# check_same_thread=False, SQLite'ın birden fazla thread ile çalışmasına izin verir (FastAPI için gereklidir).
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Veritabanı oturumlarını (session) yönetmek için bir fabrikadır.
session_manager = sessionmaker(bind=engine)

# Tüm veritabanı modellerinin (User, SessionTable vb.) miras alacağı temel sınıftır.
Base = declarative_base()

def init_db():
    """
    Veritabanını ve tanımlı olan tüm tabloları oluşturur.
    Uygulama başladığında bir kez çağrılması yeterlidir.
    """
    Base.metadata.create_all(bind=engine)
    print(f"Veritabanı {DATABASE_URL} adresinde başlatıldı.")

def get_session():
    """
    FastAPI dependency (bağımlılık) olarak kullanılır.
    Her istek (request) için yeni bir veritabanı oturumu açar ve işlem bitince kapatır.
    """
    session = session_manager()
    try:
        yield session
    finally:
        session.close()
