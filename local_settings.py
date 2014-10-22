import hashlib
DEBUG = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = "de41106c-b30c-4993-8516-62732b1c17a890943ccc-ec64-4949-bf03-cef56d66533075e7594c-59ed-4bcc-bc03-a67ce18bdc3e"
NEVERCACHE_KEY = "e9e7b45b-663f-452c-ab01-5c67fe80423139840874-b5ab-4c9c-9a13-0ddd51889eaa95898da2-7bdd-41ac-9efe-8430321b9c8a"


DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.sqlite3",
        # DB name or path to database file if using sqlite3.
        "NAME": "dev.db",
        # Not used with sqlite3.
        "USER": "",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}




