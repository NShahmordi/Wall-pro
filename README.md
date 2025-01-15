# Wall Project

Wall is a Django-based web application for managing advertisements, user accounts, and chat functionality.

## Features

- User authentication (signup, login, logout)
- Create, edit, and delete advertisements
- Bookmark advertisements
- Real-time chat functionality
- REST API for managing users, advertisements, rooms, messages, and bookmarks

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/wall.git
    cd wall
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    venv\Scripts\activate  # On Windows
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Apply the migrations:
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Create a superuser:
    ```sh
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```sh
    python manage.py runserver
    ```

## Usage

- Access the admin panel at [http://localhost:8000/admin/](http://_vscodecontentref_/0) to manage the application.
- Sign up, log in, and create advertisements.
- Bookmark advertisements and chat with other users.

## Project Structure

- [Wall](http://_vscodecontentref_/1): Main project directory
- [Main/](http://_vscodecontentref_/2): Application directory containing models, views, forms, and templates
- `templates/`: HTML templates for the application
- [static/](http://_vscodecontentref_/3): Static files (CSS, JavaScript, images)
- `media/`: Uploaded media files

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
