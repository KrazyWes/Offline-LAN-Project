# db.py
import bcrypt
import psycopg2
from psycopg2 import OperationalError
import config


def _password_bytes(password: str) -> bytes:
    """Encode password for bcrypt; bcrypt limits input to 72 bytes."""
    return password.encode("utf-8")[:72]


def _hash_password(password_plain: str) -> str:
    return bcrypt.hashpw(_password_bytes(password_plain), bcrypt.gensalt()).decode("utf-8")


def _verify_password(password_plain: str, password_hash: str) -> bool:
    return bcrypt.checkpw(_password_bytes(password_plain), password_hash.encode("utf-8"))


def get_connection():
    """Returns a connection object to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=config.DB_HOST,
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASS,
            port=config.DB_PORT,
            connect_timeout=5,
        )
        return conn
    except OperationalError as e:
        print(f"DB connection error:\n{e}")
        return None


def fetch_all(query: str, params=None):
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()
    finally:
        conn.close()


def fetch_one(query: str, params=None):
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchone()
    finally:
        conn.close()


def execute(query: str, params=None):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"DB execute error:\n{e}")
        return False
    finally:
        conn.close()


# ---------- AUTH / USERS ----------

def super_admin_exists() -> bool:
    row = fetch_one(
        "SELECT 1 FROM public.users WHERE role = %s LIMIT 1;",
        ("super_admin",)
    )
    return row is not None


def username_exists(username: str) -> bool:
    row = fetch_one(
        "SELECT 1 FROM public.users WHERE username = %s LIMIT 1;",
        (username,)
    )
    return row is not None


def create_user(username: str, password_plain: str, role: str, name: str = None) -> bool:
    password_hash = _hash_password(password_plain)
    if name is not None:
        return execute(
            """
            INSERT INTO public.users (username, password_hash, role, is_active, name)
            VALUES (%s, %s, %s, TRUE, %s);
            """,
            (username, password_hash, role, name)
        )
    return execute(
        """
        INSERT INTO public.users (username, password_hash, role, is_active)
        VALUES (%s, %s, %s, TRUE);
        """,
        (username, password_hash, role)
    )


def verify_login(username: str, password_plain: str):
    """
    Returns dict if valid login:
      {"user_id":..., "username":..., "role":...}
    Returns None if invalid.
    """
    row = fetch_one(
        """
        SELECT user_id, username, password_hash, role, is_active
        FROM public.users
        WHERE username = %s
        LIMIT 1;
        """,
        (username,)
    )
    if not row:
        return None

    user_id, uname, password_hash, role, is_active = row
    if not is_active:
        return None

    if not _verify_password(password_plain, password_hash):
        return None

    return {"user_id": user_id, "username": uname, "role": role}
