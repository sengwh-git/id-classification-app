# Identity Document Classification Application
This application features a simple React UI that allows users to submit test examples (Identity Document images) and receive the classified class via backend service built using FastAPI that makes inference using a simple CNN model. The services are wrapped into a Docker Compose configuration for deployment.

## Description
There are 3 services/containers: <br>
Model Container: Container that holds the machine learning models to deploy. <br>
Backend Service: Contains inference API built using FastAPI that receives the image from the UI and returns the prediction. <br>
Frontend: A React application that provides UI for uploading a test image and display the predicted class. <br>

## Getting Started
### Clone the repository
```
git clone https://github.com/sengwh-git/id-classification-app.git
```

### Running the services
To build the services and run the Docker containers, we will use Docker Compose by running the following command:
```
# Navigate to the app directory
cd app

# Build and run the Docker containers
docker-compose up --build
```

You should see 3 Docker images being built.

### Using the application
1. Open your web browser and enter http://localhost:3000
2. You should see the application:

<img src="home.png" width="500"/>

3. Click the dotted box or drag image to the box to upload an image.
4. Click the blue button titled "Classify ID/Passport" to generete prediction.
5. The prediction will be displayed below the uploaded image.

<img src="predict.png" width="500"/>

6. The backend API documentation is available at http://localhost:8000/docs#/