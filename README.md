# COMP639_Project_2_TUO
This app is developed based on online travel journal
app 'travlog', an app designed to capture, organize, and
relive travel memories. More features have been released in this version including earning achievements, community features, departure board, helpdesk and access premium features via subscription.

There are five user roles in this system:
- **traveller** – Regular users who can create journeys and events.
- **editor** – Can edit content across the platform.
- **admin**  – Full system control, including user and content management.
- **moderator** – Handles reports.
- **supporttech**  – Manages technical helpdesk tickets.

## Getting this Example Running

To run the example yourself, you'll need to:

1. Open the project in Visual Studio Code.
2. Create yourself a virtual environment.
3. Install all of the packages listed in requirements.txt (Visual Studio will offer to do this for you during step 2).
4. Use the [Database Creation Script](create_database.sql) to create your own copy of the **otj** database.
5. Use the [Database Population Script](populate_database.sql) to populate the **otj** data.
6. Modify [connect.py](COMP639_Project_2_TUO/connect.py) with the connection details for your local database server.
7. Run [The Python/Flask application](run.py).

## Required Software
1. Python 3.10+
2. MySQL 10.4+
3. wkhtmltopdf 0.12.6+ (for PDF generation)
