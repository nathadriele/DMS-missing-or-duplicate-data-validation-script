## DMS Missing or Duplicate Data Validation Script

### Overview
This repository contains a Python script designed to validate data replication tasks in AWS Database Migration Service (DMS). The script checks for potential issues such as missing or duplicate data in the tables being replicated. It leverages AWS SDK for Python (Boto3) to interact with AWS services and sends notifications about the status of each task to a specified API endpoint.

### Objective
The objective of this project is to automate the validation of data replication integrity across multiple AWS Database Migration Service (DMS) tasks. The provided Python script achieves this by performing the following actions:
- `Processing Multiple DMS Replication Tasks`: Iterates over a predefined set of DMS replication tasks identified by their Amazon Resource Names (ARNs), which are specified in the tasks dictionary within the script.
- `Validating Task Existence`: For each task, the script checks if the replication task exists in AWS DMS. If a task is not found, it logs a warning message and proceeds to the next task without interrupting the entire validation process.
- `Retrieving Table Statistics`: For existing tasks, it retrieves detailed table statistics using the `describe_table_statistics` method from the AWS DMS client. This information includes operation counts like inserts, updates, and deletes, as well as their applied counterparts.
- **`Detecting Missing or Duplicate Data`**:
   - Missing Data: Compares the expected number of operations `(inserts, updates, deletes)` with the applied operations `(applied_inserts, applied_updates, applied_deletes)`. If the expected operations exceed the applied ones, it identifies potential missing data.
   - `Duplicate Data`: If the applied operations exceed the expected ones, it flags potential duplicate data.
- **`Generating Event Notifications`**:
   - `Event Naming`: Constructs an event name based on the task name and the type of issue detected `(e.g., task1_dms_missing, task2_dms_duplicates, or task3_dms_no_issues)`.
   - `Status Codes`: Assigns a status code where 0 indicates issues detected `(missing or duplicate data)` and 1 indicates no issues.
   - `API Integration`: Sends a POST request to a specified API endpoint `(NOTIFIER_URL)` with the event name and status code in JSON format to notify stakeholders of the validation results.

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
- `Error Reduction`: Identifies and mitigates data type mismatches early, reducing errors in downstream processes.
- `Automated Monitoring`: Automates data validation, allowing Data Engineers to focus on more complex tasks.
- `Proactive Alerts`: Sends notifications about validation results, enabling timely interventions to maintain data quality.
