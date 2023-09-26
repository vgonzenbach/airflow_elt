# Airflow ELT Pipeline

## Introduction

This repository contains an ELT (Extract, Load, Transform) pipeline built using Apache Airflow. The pipeline is designed to move data from a source (S3) to a Redshift data warehouse, performing transformations along the way.

## Technologies Used

- Python
- Apache Airflow
- SQL
- AWS Redshift

## Setup

### Prerequisites

- Python 3.x
- Apache Airflow
- AWS Redshift

### Installation Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/vgonzenbach/airflow_elt.git
    ```

2. Navigate to the project directory:
    ```bash
    cd airflow_elt
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Update the `airflow.cfg` with your specific configurations and rename it to `airflow.cfg`.

5. Run the setup scripts to initialize the database:
    ```bash
    ./setup/init_db.sh
    ```

## Usage

1. Start the Airflow web server:
    ```bash
    ./start-airflow.sh
    ```

2. Open the Airflow UI and trigger the DAG.

## Contributing

Feel free to fork the project and submit a pull request with your changes!

## License

This project is licensed under the MIT License.

