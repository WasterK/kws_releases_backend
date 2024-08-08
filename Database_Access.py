import psycopg2


class DatabaseAccess:
    def __init__(self, database_url: str) -> None:
        try:
            self.conn = psycopg2.connect(database_url)
            self.cur = self.conn.cursor()
            print("Connected to database")
        except psycopg2.Error as e:
            print(f"Database connection error : {e}")
            raise psycopg2.DatabaseError("Connection error occurred")
        
    def close_connection(self):
        if self.conn:
            self.conn.close()

    def create_table(self, table_name: str) -> None:
        try:
            create_table_query = f"""
                CREATE TABLE IF NOT EXISTS public.users
                (
                    user_id integer NOT NULL DEFAULT nextval('users_user_id_seq'::regclass),
                    username character varying(50) COLLATE pg_catalog."default" NOT NULL,
                    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
                    unique_id character varying(255) COLLATE pg_catalog."default",
                    email_id character varying(255) COLLATE pg_catalog."default",
                    profile_photo character varying(255) COLLATE pg_catalog."default",
                    CONSTRAINT users_pkey PRIMARY KEY (user_id),
                    CONSTRAINT users_unique_id_key UNIQUE (unique_id),
                    CONSTRAINT users_username_key UNIQUE (username)
                )
            """
            self.cur.execute(create_table_query)
            self.conn.commit()
            print(f"Table '{table_name}' created successfully.")
        except psycopg2.Error as e:
            print(f"Error creating table '{table_name}': {e}")

    def isUsernameExists(self, username):
        try:
            query = "SELECT count(username) FROM users WHERE email_id = %s"
            self.cur.execute(query, (username,))
            output = self.cur.fetchone()
            if output[0] > 0:
                return True
            return False
        except psycopg2.Error as e:
            return None
        
    def create_new_user(self, username, unique_id, email_id, profile_photo):
        try:
            query = "INSERT INTO users(username, unique_id, email_id, profile_photo) VALUES(%s, %s, %s, %s)"
            self.cur.execute(query, (username, unique_id, email_id, profile_photo))
            self.conn.commit()
        except psycopg2.Error as e:
            print(f"error while createing user, Error: {e}")
            return None

    def user_validation(self, username: str, password: str) -> bool:
        try:
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            self.cur.execute(query, (username, password))
            user = self.cur.fetchone()
            if user:
                print("User validated successfully.")
                return True
            else:
                print("Invalid username or password.")
                return False
        except psycopg2.Error as e:
            print("Error validating user:", e)
            return False

# db = DatabaseAccess(database_url="postgresql://admin:admin123@0.tcp.in.ngrok.io:12537/kws_releases_backend")
# db.get_all_devices('115762642791498046873')