# GrainCircuit

GrainCircuit is a full-fledged, user-friendly web application for managing bookmarks and URLs. Designed with efficiency and simplicity in mind, it offers users an elegant solution to organise, categorise, and interact with their bookmarks seamlessly.

## Features

- **Registration and Authentication**: Secure user registration and login.
- **Sidebar Navigation**: Intuitive menu for quick access to app sections.
- **Account Management**: Update profile information, reset passwords, and manage account settings.
- **Bookmarks Management**: Add, edit, search, and delete bookmarks with ease.
- **Category Management**: Customise categories with names and colours for better organisation.
- **Drag-and-Drop Sorting**: Intuitive drag-and-drop functionality for rearranging bookmarks and categories.
- **Search Bar**: Quickly locate bookmarks by title, category, or tags.
- **Pagination**: Efficiently handle large collections of bookmarks.
- **Mobile Responsiveness**: Fully optimised for mobile and desktop devices.

## Project Overview

GrainCircuit is more than just a bookmark manager. It is a platform that transforms how users interact with their saved URLs:

- **Visual Organisation**: Bookmarks are displayed as interactive, visually rich cards featuring metadata such as images, titles, categories, and dates.
- **Customisation**: Users can personalise their experience by creating custom categories, assigning colours, and adding tags.
- **Efficient Workflow**: Default categories like "Unsorted" and "Trash" help keep bookmarks organised automatically, with powerful search and sorting features to streamline navigation.

The application is built with Django on the backend, complemented by JavaScript for dynamic features like drag-and-drop functionality and real-time updates. It uses server-side rendering for initial pages while integrating dynamic JavaScript for enhanced interactivity.

## Technology Stack

- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: PostgreSQL
- **Containerisation**: Docker
- **Deployment**: Azure Web App (using Azure Container Registry)
- **Storage**: Azure Blob Storage for static and media files
- **Version Control**: GitHub
- **Testing**: Python `unittest`
- **CI/CD**: GitHub Actions for automated build and deployment workflows

## Deployment Details

GrainCircuit is hosted on Microsoft Azure using a fully containerised environment:

- **Docker**: The app is dockerised to ensure consistent builds and deployments.
- **Azure Blob Storage**: Static and media files are served securely via Azure Blob Storage.
- **PostgreSQL**: Azure Database for PostgreSQL handles reliable, scalable data storage.
- **Azure Web App**: The app is deployed using Azure Web App for Containers.

## Getting Started

### Prerequisites

- Python 3.12+
- Docker
- PostgreSQL
- Pipenv for managing Python dependencies
- Azure CLI (for deployment)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/gosuarez/graincircuit.git
   cd graincircuit
   ```

2. Install dependencies:

    ```bash
    pipenv install --dev
    ```

3. Set up environment variables: Create `.env.dev` or `.env.prod` files based on the provided `.env.example.` Configure Azure, PostgreSQL, and other settings based on your environment.

4. Run migrations:

    ```bash
    python manage.py migrate
    ```

5. Start the development server:

    ```bash
    python manage.py runserver
    ```

6. Access the application locally: Navigate to `http://127.0.0.1:8000` in your web browser.

### Docker Deployment

1. Build the Docker image:

    ```bash
    docker build -f Dockerfile.prod -t graincircuit-web:latest .
    ```

2. Run the container:

    ```bash
    docker-compose -f docker-compose.prod.yml up
    ```

### Azure Deployment

1. Push the Docker image to Docker Hub:

    ```bash
    docker push <your-dockerhub-username>/graincircuit-web:latest
    ```

2. Use the provided GitHub Actions workflow to automate deployment to Azure.

3. Access the application at your Azure Web App URL.

### Testing

Run the test suite using:

```bash
python manage.py test
```

The suite includes unit tests for forms, models, and views to ensure the app functions as expected.

## Feedback

If you have any questions or feedback, feel free to reach out to me at <contact@gosuarez.com>.

## License

This project is licensed under the [MIT License](LICENSE).

## Author

[Gonzalo Suarez](https://www.gosuarez.com) - GrainCircuit is a showcase of my ability to design, build, and deploy robust, user-friendly web applications. Thank you for visiting!
