# My Portfolio

Welcome to my portfolio website! This repository contains the source code for my personal portfolio, which showcases information about me, my projects, and blogs I've uploaded.

## Website Link

You can visit my portfolio website https://rohitweb.pythonanywhere.com/ .

## About the Website

This portfolio website contains the following sections:
- **About Me**: Information about my background, skills, and interests.
- **Projects**: A showcase of the projects I have worked on, with detailed descriptions and links to the respective repositories.
- **Blogs**: A collection of blogs I have written on various topics.

## Running the Project Locally

To run this project locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Rohitthakan/my_portfolio.git
    cd my_portfolio
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv portfolio_venv
    source portfolio_venv/bin/activate  # On Windows use `portfolio_venv\Scripts\activate`
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations**:
    ```bash
    python manage.py migrate
    ```

5. **Collect static files**:
    ```bash
    python manage.py collectstatic
    ```

6. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

## Collecting Static Files

To collect static files, run the following command in the virtual environment:
```bash
python manage.py collectstatic
