# travel-blog
Travel Blog for S+J

## Project Description

This project is a travel blog with the following features:

- Signup and Login users
- Published Notes and Journals are publicly viewable
- Add and delete items from a travel bucket list
- Create journal entries for each country visited
- Add text and photos to journal entries
- Edit and delete journal entries

The project is built using:
- Flask: a Python web framework
- MongoDB: a NoSQL database
- Flask-WTF: a form validation library
- Flask-Login: a user authentication library
- Front end: HTML, CSS, and JavaScript
- Cursor AI: to generate code boilerplate, provide suggestions, and help with debugging

## Project Structure

The project is organized as follows:

- `app.py`: The main application file that initializes the Flask app and connects to the database.
- `models.py`: The models file that defines the data models for the application.
- `routes.py`: The routes file that defines the routes for the application.
- `templates/`: The templates folder that contains the HTML templates for the application.
- `static/`: The static folder that contains the static files for the application.


## Design Choices

The project incorporates several key design decisions to enhance functionality, scalability, and user experience:

1. **Database Migration**: Switched from a SQL database to MongoDB
   - Provides greater flexibility for adding new content types (e.g., images) without requiring database schema updates
   - Allows for easier adaptation to changing data requirements as the project evolves

2. **Collaborative Content**: Shared journals and notes
   - All users contribute to a single, collaborative space for each country
   - Enhances the community aspect of the travel blog
   - Only content owners can edit or delete their own entries, maintaining individual accountability

3. **Public Viewing, Authenticated Editing**: 
   - Content is viewable by all visitors, including non-logged-in users
   - Only authenticated users can add, edit, or delete content
   - Balances the public nature of a travel blog with the need for content control

4. **Modular JavaScript**: 
   - Core functionality written generically to support multiple countries (Vietnam, Thailand, etc.)
   - Easily extendable to accommodate future country additions without significant code changes

5. **Security Considerations**:
   - Implements user authentication to protect content creation and modification
   - Ensures that sensitive operations (e.g., deleting entries) are only available to content owners

6. **Responsive Design**:
   - Utilizes responsive CSS to ensure a good user experience across various device sizes
   - Hero images, navbar, and feeds are optimized for both mobile and desktop browsers
   - Enhances accessibility and usability for users on different devices

These design choices aim to create a flexible, user-friendly, and scalable travel blog platform that can grow and adapt to future needs while maintaining a focus on collaborative content creation and public accessibility.

## Installation and Setup

To set up and run this project, follow these steps:

1. **Install MongoDB**:
   - For server installation, follow the official MongoDB installation guide for your operating system: https://docs.mongodb.com/manual/installation/
   - For local development, you can install MongoDB Compass from: https://www.mongodb.com/try/download/compass

2. **Start MongoDB**:
   - If using a server installation, ensure the MongoDB service is running.
   - If using MongoDB Compass, open the application and connect to your database.

3. **Create a Virtual Environment** (Recommended):
   It's best to use a virtual environment to manage dependencies. You can use either venv or conda:

   Using venv:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

   Or using conda:
   ```
   conda create --name travel_blog python=3.8
   conda activate travel_blog
   ```

4. **Install Requirements**:
   Once your virtual environment is activated, install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. **Run the Application**:
   Start the Flask application by running:
   ```
   python main.py
   ```

   The application should now be running on `http://localhost:5000` (or another port if specified).

Remember to set up your environment variables or configuration files as needed before running the application. This may include database connection strings, secret keys, or other sensitive information not included in the public repository.

