import os
from sqlalchemy import create_engine, text

def get_engine():
    """Crea y retorna el engine de conexión a PostgreSQL."""
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5432')
    database = os.getenv('DB_NAME', 'olist_db')
    user = os.getenv('DB_USER', 'olist_user')
    password = os.getenv('DB_PASSWORD', 'olist_pass')
    
    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    return create_engine(connection_string)

def test_connection():
    """Prueba la conexión a la base de datos."""
    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            print("Conexion exitosa a PostgreSQL!")
            print(f"Version: {result.fetchone()[0]}")
            return True
    except Exception as e:
        print(f"Error de conexion: {e}")
        return False

if __name__ == "__main__":
    test_connection()
