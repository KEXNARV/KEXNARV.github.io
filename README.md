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
- User accounts stored in `users.enc` so credentials can be committed to the repository. The contents are Base64 encoded and updated via the Users page using a GitHub token that is kept only in `sessionStorage`. Login status is kept in `sessionStorage` so credentials aren't saved locally after the tab is closed.
- A default root account (`Kex`/`JouleNW2027`) is always added if missing.

### Managing Users
1. Sign in as `Kex` and open `usuarios.html` from the dashboard.
2. The page will request your personal GitHub token the first time it needs to save changes.
3. Added or modified users are written back to `users.enc` in the repository using that token.

## Usage Guidelines
- Ensure that the Java environment is set up for running the backend logic.
- Modify the `main.css` file to customize the appearance of the dashboard.
- Update the `Dashboard.java` file to implement additional backend functionalities as needed.
