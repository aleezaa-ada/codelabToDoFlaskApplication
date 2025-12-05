# codelabToDoFlaskApplication
A simple Flask web application where users can register, log in, and manage their tasks.  
You can create, edit, complete, and delete tasks through a clean user interface.

You can run this project in **GitHub Codespaces** or locally on your machine.


1. Open the repository
2. In project root, run:
    
    for macOS / Linux / GitHub Codespaces:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
    Windows (PowerShell):
    ```bash
    python -m venv venv
    venv\Scripts\Activate.ps1
    ```

3. then run:
    ```bash
    pip install -r requirements.txt
    ```

4. then run:

    for macOS / Linux / GitHub Codespaces:
    ```bash
    cp .env_sample .env
    ```
    or for Windows (powershell)
    ```bash
    copy .env_sample .env
    ```

5. Finally run:

    for macOS / Linux / GitHub Codespaces:
    ```bash
    export FLASK_APP="app:create_app"
    flask run
    ```
    or for windows (powershell):
    ```bash
    $env:FLASK_APP = "app:create_app"
    flask run
    ```

6. then just click the link to open the app.

### Using the Application
- Register
    - Click Register
    - Create a username and password

- Log In
    - Enter the same username & password
    - You’ll be redirected to the dashboard

- Navigate
    - Use the nav bar:
        - Home — dashboard
        - View Tasks — see your tasks
        - New Task — add a task
        - Logout — end session
    
- Manage Tasks 
    - Create a task
    - Edit a task (title or completion status)
    - Delete a task
    - Completed tasks appear crossed out

### Running tests

with the virtual env active run:
```bash
pytest -v
```

to run test for coverage
```bash
pytest --cov=app --cov-report=term-missing
```

### Hooks and github actions implemented
- added pre-push hook to check code coverage 
- added github actions to check for any linting errors after being pushed to main

### What can be better
- stronger authentication : adding password confirmation, session timeouts
- Separate frontend: easier to create components and test front-end pages with a front-end framework in place like react, also would be good to address accesibility concerns using aria-labels and axe devTools
- dashboard insights: showing stats like tasks completed today, tasks remaining etc.
- improve GitHub Actions and git hooks: run a linting checker in a pre-commit hook and run code-coverage checks in a pre-push hook, so no code with linting issues or low coverage ever makes it into main. In GitHub Actions, split linting and testing into separate jobs, add caching to speed up installs, enforce coverage thresholds, and upload coverage reports for easier debugging.