# Company Dashboard

## Overview
The Company Dashboard is a web application designed to provide an interactive interface for managing and visualizing company data. It serves as a central hub for accessing various functionalities related to company operations.

## Project Structure
```
company-dashboard
├── src
│   ├── index.html          # Main HTML document for the dashboard
│   ├── styles              # Folder containing CSS styles
│   │   └── main.css        # Styles for the dashboard
│   └── java                # Folder containing Java backend logic
│       └── Dashboard.java  # Java class for handling backend operations
└── README.md               # Documentation for the project
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd company-dashboard
   ```
3. Open `src/index.html` in a web browser to view the dashboard.

## Features
- Interactive data visualization
- User-friendly interface
- Backend logic implemented in Java for data processing
<<<<<<< HEAD
- User accounts stored in `users.enc` so credentials can be committed to the repository. The contents are Base64 encoded and can be updated from the Users page using a GitHub token.
=======
- Login is handled client-side using Firebase Authentication. Configure your Firebase project in `firebase-config.js`.
>>>>>>> codex/modificar-inicio-de-sesión-para-compatibilidad-con-github-pa

## Usage Guidelines
- Ensure that the Java environment is set up for running the backend logic.
- Modify the `main.css` file to customize the appearance of the dashboard.
- Update the `Dashboard.java` file to implement additional backend functionalities as needed.