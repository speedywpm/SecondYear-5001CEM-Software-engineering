# Book shop + checkout API

A simple, functional online book shop built using Flask, HTML, CSS, and SQLAlchemy. Users can register, login, view and buy products, and manage stock items.

## Features

* Registration and login system
* Storefront for browsing and purchasing books
* Admin panel for managing stock items
* Shopping cart functionality
* Basic security features

## Installation

1. Clone the repository or download the .zip file of the project.
2. Extract the contents of the .zip file to your desired location.
3. Open your terminal and navigate to the extracted folder using the cd command.
4. Run the following commands to install the necessary dependencies:

`pip install Flask` <br />
`pip install Flask-SQLAlchemy` <br />
`pip install flask-cors` <br />
`sudo apt update` <br />
`sudo apt-get install python3-venv` <br />
`python3 -m venv venv` <br />
`. venv/bin/activate` <br />
`cd SHOPPING_CART_FLASK` <br />
`export FLASK_APP=main` <br />
`flask run --host=0.0.0.0` <br />

5. Follow the instructions provided in the repository for setting up the checkout system and updating the necessary configurations.
6. To run the application, use the following command:
`env FLASK_APP=payments FLASK_ENV=development ./venv/bin/flask run --host=0.0.0.0`
7. Open your browser and navigate to http://localhost:5000 to access the application.

## Testing
The application has been tested for basic functionality, including:

* Registration and login
* Browsing the storefront
* Adding and removing items from the shopping cart
* Checking out

Please note that some features, such as removing stock items and handling duplicate ISBN numbers, have not been implemented or tested. Additionally, security measures are basic and improvements can be made.

## Quality Assurance

This project has been developed using HTML, CSS, Flask, Python, and SQLAlchemy. The application has been tested for basic functionality and improvements can be made in future updates. Please refer to the repository for a detailed quality assurance statement and external QA evaluation.

## Documentation

All necessary documentation, including installation guides, testing regimes, quality assurance statements, and user manuals can be found in the repository. Please refer to the provided documents for a comprehensive understanding of the project and its features.

## Credits

* Gurvinder (Student ID: 10248274): Helped with common issues and provided guidance on working with virtual environments.
* Luke (Student ID: 10107753): Assisted with Flask concepts and provided explanations for various functions.

## License

This project is licensed under the MIT License.
