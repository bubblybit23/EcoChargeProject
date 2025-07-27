# EcoCharge

EcoCharge is a project for Lightweight Solutions (Philippines) that provides a platform for optimizing energy consumption. It uses Django for core services and FastAPI for AI optimization.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Python 3.12
* Node.js 16
* Pip
* Npm

### Installing

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/EcoCharge.git
   ```

2. **Set up the backend:**

   ```bash
   cd EcoCharge/backend
   pip install -r requirements.txt
   cd core
   python manage.py migrate
   python manage.py runserver
   ```

3. **Set up the frontend:**

   ```bash
   cd EcoCharge/frontend/dashboard
   npm install
   npm run serve
   ```

## Deployment

The project is deployed to AWS Manila using a CI/CD pipeline with GitHub Actions.

## Built With

* [Django](https://www.djangoproject.com/) - The web framework for the core services
* [FastAPI](https://fastapi.tiangolo.com/) - The web framework for the AI optimization
* [Vue.js](https://vuejs.org/) - The progressive JavaScript framework for the frontend
* [Watttime API](https://www.watttime.org/api-documentation/) - The API for real-time energy data

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Jules** - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
