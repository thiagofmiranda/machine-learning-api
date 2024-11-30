# Machine Learning API with Docker

This project provides a **Machine Learning API** that serves machine learning models through a robust and scalable web interface. The API is built using Docker and Docker Compose and is designed to serve predictions based on models imported from an external repository: [Machine Learning Models Repository](https://github.com/thiagofmiranda/machine-learning-models).

## Project Overview

### **API**:
   - The **API** is the core service of the application, responsible for accepting requests, processing them, and returning predictions. It is built to handle machine learning tasks, such as scoring and predictions.
   - The API imports models from the [machine-learning-models repository](https://github.com/thiagofmiranda/machine-learning-models) located in the `models` folder. These models are loaded and used to process incoming data and return predictions.
   - The API is containerized, built from the provided source code, and serves as the backbone of the application, interacting with other services like Redis and NGINX.
   - The API is deployed with Docker Compose and is set to be easily scalable for handling large volumes of requests.

### **Redis**:
   - Redis is used as a caching layer to store and retrieve results from previous predictions, speeding up responses and reducing unnecessary recomputations.
   - The Redis service is configured with persistence and health checks, ensuring reliability and stability during runtime.
   - It integrates seamlessly with the API to store machine learning results.

### **NGINX**:
   - NGINX serves as a reverse proxy, handling incoming HTTP requests and forwarding them to the API service.
   - It is configured with a custom `nginx.conf` for efficient load balancing and routing.
   - Logs generated by NGINX are stored in a dedicated volume for easy access and management.


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/thiagofmiranda/machine-learning-api.git
   cd machine-learning-api
   ```

2. Install Docker:
    https://docs.docker.com/get-started/introduction/get-docker-desktop/

3. Use Docker Compose to set up the environment:
   ```bash
   docker volume create nginx_logs
   docker-compose up --build
   ```

### Stack Running
![docker](images/docker.png)


## Usage

Once the API is running, you can access the endpoints:
- **health check**: `/hc` API health check
- **list-models**: `/list-models` list models avaliable
- **Model Predict**: `/<model>/predict` make predictions with any trained model

First, run the health check:
```bash
curl http://localhost:3000/hc
```

List available ML models to obtain predictions:
```bash
curl http://localhost:3000/hc
```

Finally, You may run the predict command on Linux:
```bash
curl -X POST http://localhost:3000/language-detection/predict/ -d '{"input_data": {"text": "My name is Thiago"}}' 
```

or on Windows:
```powershell
$headers = @{
    "Content-Type" = "application/json"
}
Invoke-WebRequest -Uri "http://localhost:3000/language-detection/predict" -Method POST -Body '{"input_data": {"text": "My name is Thiago"}}' -Headers $headers
```

## Key Features:

- **Model Integration**: The API dynamically imports machine learning models from the [Machine Learning Models repository](https://github.com/thiagofmiranda/machine-learning-models).
- **Caching**: Redis provides a caching layer to improve performance and reduce unnecessary computations.
- **Scalable**: The architecture is built for scalability with Docker and Docker Compose, making it easy to scale the API service.
- **Logging and Monitoring**: NGINX handles request logging and routing, and the logs are persisted for monitoring and debugging.

## License

This project is licensed under the [MIT License](LICENSE).
