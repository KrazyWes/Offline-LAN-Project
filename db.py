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


def connection_ok() -> bool:
    """Quick check if database is reachable."""
    conn = get_connection()
    if not conn:
        return False
    conn.close()
    return True


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
    except Exception as e:
        print(f"DB fetch_all error:\n{e}")
        return []
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
    except Exception as e:
        print(f"DB fetch_one error:\n{e}")
        return None
    finally:
        conn.close()


_last_execute_error = None


def get_last_error() -> str | None:
    """Return the last execute() error message, or None."""
    return _last_execute_error


def execute(query: str, params=None, require_affected: bool = False):
    """
    Execute a query. Returns True on success, False on error.
    If require_affected=True, returns False if no rows were affected (useful for UPDATE/DELETE).
    """
    global _last_execute_error
    _last_execute_error = None
    conn = get_connection()
    if not conn:
        _last_execute_error = "Cannot connect to database"
        return False
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            rowcount = cur.rowcount
        conn.commit()
        if require_affected and rowcount == 0:
            _last_execute_error = "No rows affected"
            return False
        return True
    except Exception as e:
        conn.rollback()
        _last_execute_error = str(e)
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
        "SELECT 1 FROM public.users WHERE username = %s AND role != %s LIMIT 1;",
        (username, "super_admin")
    )
    return row is not None


def create_user(username: str, password_plain: str, role: str, name: str) -> bool:
    """Create a new user. All fields are required (name is NOT NULL in DB)."""
    password_hash = _hash_password(password_plain)
    role = role or "cashier"
    name = name or username  # fallback to username if name is empty
    return execute(
        """
        INSERT INTO public.users (username, password_hash, role, is_active, name, created_at)
        VALUES (%s, %s, %s, FALSE, %s, NOW());
        """,
        (username, password_hash, role, name)
    )


def verify_login(username: str, password_plain: str):
    """
    Returns dict if valid login:
      {"user_id":..., "username":..., "role":...}
    Returns None if invalid (user not found or wrong password).
    Note: is_active is not checked here—it tracks session state (login/logout).
    Login fails only if user is deleted (not found) or password is wrong.
    """
    row = fetch_one(
        """
        SELECT user_id, username, password_hash, role
        FROM public.users
        WHERE username = %s
        LIMIT 1;
        """,
        (username,)
    )
    if not row:
        return None

    user_id, uname, password_hash, role = row

    if not _verify_password(password_plain, password_hash):
        return None

    return {"user_id": user_id, "username": uname, "role": role}


def update_last_active(user_id) -> bool:
    """Update user's last_active time and set is_active (on login)."""
    return execute(
        """
        UPDATE public.users
        SET last_active = CURRENT_TIME, is_active = TRUE
        WHERE user_id = %s;
        """,
        (user_id,)
    )


def deactivate_user(user_id) -> bool:
    """Set is_active to false and update last_active (on logout)."""
    return execute(
        """
        UPDATE public.users
        SET is_active = FALSE, last_active = CURRENT_TIME
        WHERE user_id = %s;
        """,
        (user_id,)
    )


# ---------- ACCOUNTS (excludes super_admin for security) ----------

ROLES_FOR_ACCOUNTS = ("administrator", "cashier", "monitor", "operator_a", "operator_b")
ROLE_DISPLAY = {"administrator": "Administrator", "cashier": "Cashier", "monitor": "Monitor", "operator_a": "Operator A", "operator_b": "Operator B"}


def fetch_users_excluding_super_admin():
    """
    Fetch all users except super_admin. Returns list of dicts:
    [{"user_id", "username", "name", "role", "is_active", "last_active"}, ...]
    """
    rows = fetch_all(
        """
        SELECT user_id, username, name, role, is_active, last_active
        FROM public.users
        WHERE role != %s
        ORDER BY CASE role
            WHEN 'administrator' THEN 1
            WHEN 'operator_a' THEN 2
            WHEN 'operator_b' THEN 3
            WHEN 'monitor' THEN 4
            WHEN 'cashier' THEN 5
            ELSE 6
        END ASC, COALESCE(name, username) ASC;
        """,
        ("super_admin",)
    )
    return [
        {
            "user_id": r[0],
            "username": r[1],
            "name": r[2],
            "role": r[3],
            "is_active": r[4],
            "last_active": r[5],
        }
        for r in rows
    ]


def update_user_account(user_id: int, username: str, name: str, role: str, password_plain: str = None) -> bool:
    """Update user. Does not allow updating super_admin."""
    role = str(role or "cashier")
    if role not in ROLES_FOR_ACCOUNTS:
        return False
    if password_plain:
        password_hash = _hash_password(password_plain)
        return execute(
            """
            UPDATE public.users
            SET username = %s, name = %s, role = %s, password_hash = %s
            WHERE user_id = %s AND role != %s;
            """,
            (username, name, role, password_hash, user_id, "super_admin"),
            require_affected=True,
        )
    return execute(
        """
        UPDATE public.users
        SET username = %s, name = %s, role = %s
        WHERE user_id = %s AND role != %s;
        """,
        (username, name, role, user_id, "super_admin"),
        require_affected=True,
    )


def delete_user_account(user_id: int) -> bool:
    """Delete user. Does not allow deleting super_admin."""
    return execute(
        "DELETE FROM public.users WHERE user_id = %s AND role != %s;",
        (user_id, "super_admin"),
        require_affected=True,
    )


def fetch_cashiers():
    """
    Fetch all users with role='cashier'. Returns list of dicts:
    [{"user_id", "username", "name", "is_active", "last_active"}, ...]
    """
    rows = fetch_all(
        """
        SELECT user_id, username, name, is_active, last_active
        FROM public.users
        WHERE role = %s
        ORDER BY COALESCE(name, username) ASC;
        """,
        ("cashier",)
    )
    return [
        {
            "user_id": r[0],
            "username": r[1],
            "name": r[2],
            "is_active": r[3],
            "last_active": r[4],
        }
        for r in rows
    ]
