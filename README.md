## DMS Missing or Duplicate Data Validation Script

### Overview
This repository contains a Python script designed to validate data replication tasks in AWS Database Migration Service (DMS). The script checks for potential issues such as missing or duplicate data in the tables being replicated. It leverages AWS SDK for Python (Boto3) to interact with AWS services and sends notifications about the status of each task to a specified API endpoint.

### Table of Contents
- Prerequisites
- Installation
- Usage
- Code Explanation

### Prerequisites
Before running the script, ensure you have the following:

- Python 3.7 or higher installed.
- AWS account with access to DMS.
- AWS credentials configured in your environment.
- Access to the API endpoint for notifications.

### Installation
1. Clone this repository to your local machine:

```py
git clone https://github.com/nathadriele/DMS-missing-or-duplicate-data-validation-script.git
cd dms-data-validation
```

2. Install the required dependencies:

```py
pip install -r requirements.txt
```

### Usage
1. Set up AWS Credentials: Ensure your AWS credentials are set in your environment variables. You can configure them by running:

```py
export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
```

2. Run the Script:

```py
python dms_data_validation.py
```

The script will iterate over the specified DMS tasks, validate the data, and send notifications based on the results.

### Code Explanation
This Python script interacts with AWS Database Migration Service (DMS) to validate the integrity of data replicated between different database environments. Below is a detailed explanation of the key components and functions of the script:

- `Connect to AWS DMS`: Utilizes AWS credentials to authenticate and connect to DMS.
- `Validate Replication Tasks`: Checks the status of specified DMS tasks and retrieves table statistics for validation.
- `Identify Data Issues`: Detects potential missing or duplicate data based on the difference between expected and applied operations.
- `Send Notifications`: Communicates validation.

### Imports and Setup
- `Logging`: Used for logging messages to the console, facilitating monitoring and debugging of the code.
- `Boto3`: AWS SDK for Python, used to connect to DMS and perform replication task management operations.
- `Requests`: Library for making HTTP requests, used here to send notifications about the status of replication tasks.
- `Mage.ai Secrets`: Tool for managing secrets like AWS credentials, which are not defined directly in the code.

#### Constants
- `AWS_REGION`: Defines the AWS region in which the DMS client operates. By default, it is set to us-east-1, but it can be changed as needed.
- `NOTIFIER_URL`: Endpoint where notifications about the results of task validations are sent.

#### Data Loader Function
The main function, load_data, is responsible for loading and validating data from DMS tasks. Decorated with `@data_loader`, it is a Mage AI platform standard for indicating data loading functions.

#### DMS Tasks
Tasks ARN Dictionary: Maps task names to their respective ARNs (Amazon Resource Names). ARNs are unique identifiers that reference replication tasks in DMS.

#### AWS DMS Client
`DMS Client Initialization`: Creates a DMS client using AWS credentials obtained from environment variables or secret management. This allows the script to interact with the DMS service to manage and monitor replication tasks.

### Task Processing
- The script iterates over the defined tasks and performs the following operations:
    - Task Existence Validation: Uses describe_replication_tasks to check if each task exists. If a task is not found, a warning is logged.
    - Table Statistics: Retrieves table statistics using describe_table_statistics, which provides data on insert, update, and delete operations in the involved tables.

### Validation Logic
- Data Validation: Compares planned and applied operations (inserts, updates, deletes) to identify possible missing or duplicate data.
    - Missing Data: Checks if there are planned operations that were not applied, suggesting data loss.
    - Duplicate Data: Checks if applied operations exceed planned ones, indicating data duplication.

### Notification
- After validating the data, the script sends notifications based on the results:
    - Event Name and Status: Defines the event name and status (0 for detected issues, 1 for no issues) and sends a POST request to NOTIFIER_URL.
    - HTTP Response Handling: Logs an error if the request fails and confirms successful notification delivery.

### Testing
The script includes basic testing functions to ensure the data loader function works as expected.

### Metadata Configuration
The metadata.yaml file contains the configuration for the Mage.ai block used in this project. It defines the block's properties, execution type, and other settings that control how the data validation process is executed.

### Trigger Configuration
The triggers.yaml file defines the schedule and settings for triggering the data validation pipeline. It specifies the frequency (@daily), start time, and other settings necessary for automating the execution of the validation process.

### Contribution to Data Engineering
This project plays a vital role in Data Engineering by ensuring that the data stored in PostgreSQL tables conforms to the expected data types. Data Engineers rely on accurate and reliable data to build data pipelines, perform ETL processes, and generate meaningful insights. By validating data types:
- Error Reduction: Identifies and mitigates data type mismatches early, reducing errors in downstream processes.
- Automated Monitoring: Automates data validation, allowing Data Engineers to focus on more complex tasks.
- Proactive Alerts: Sends notifications about validation results, enabling timely interventions to maintain data quality.
