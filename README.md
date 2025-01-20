![alt text](sample-1.png)

### The frontend is in index.html, the backend is in app.py, and the styling is in style.css. The icons are now rounded rectangular buttons without borders.

Before running the app, please make sure to:

Provide Logo and Icon Images: Replace "company_logo.png", "food_icon.png", "transport_icon.png", and "mobile_icon.png" in index.html with the actual paths to your logo and icon images.

Set Environment Variables: Set the following environment variables with your PostgreSQL database credentials:

>- PGHOST: Your database host
>- PGPORT: Your database port
>- PGUSER: Your database username
>- PGPASSWORD: Your database password
>- PGDATABASE: Your database name

Create Database Table: Create the **reimbursements** table in your PostgreSQL database with the following columns:


1. name (text)
2. date (date)
3. time (time)
4. amount (numeric)
5. reason (text)
6. category (text)
7. restaurant_name (text)
8. destination (text)
9. distance (numeric)


-- Connect to your PostgreSQL database
<code>
psql -d your_database_name
</code>


-- Create the reimbursements table
<code>
CREATE TABLE reimbursements (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    reason TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    restaurant_name VARCHAR(255),
    destination VARCHAR(255),
    distance NUMERIC(10, 2)
);
</code>


Install Libraries: Make sure you have the psycopg2 and Flask libraries installed (pip install psycopg2 Flask).

You can then run the app using python app.py. The app will be accessible at port 5000.