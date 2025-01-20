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


Install Libraries: Make sure you have the psycopg2 and Flask libraries installed (pip install psycopg2 Flask).

You can then run the app using python app.py. The app will be accessible at http://127.0.0.1:5000/.