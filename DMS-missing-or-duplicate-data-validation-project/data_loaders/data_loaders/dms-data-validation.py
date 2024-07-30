import logging
import os
from typing import Dict, Any

import boto3
import requests

from mage_ai.data_preparation.shared.secrets import get_secret_value

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

AWS_REGION = 'us-east-1'
NOTIFIER_URL = 'https://api.notifier.engineering.test.com/events'

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data(*args, **kwargs) -> Dict[str, Any]:
    """Loads DMS tasks and validates data replication integrity."""

    # Task ARNs dictionary
    tasks = {
        'task1': 'arn:aws:dms:task1',
        'task2': 'arn:aws:dms:task2',
        'task3': 'arn:aws:dms:task3',
        'task4': 'arn:aws:dms:task4',
    }

    # Initialize AWS DMS client
    client = boto3.client(
        'dms',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', get_secret_value('aws_access_key_id')),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', get_secret_value('aws_secret_access_key')),
        region_name=AWS_REGION,
    )

    for task_name, task_arn in tasks.items():
        try:
            client.describe_replication_tasks(Filters=[{'Name': 'replication-task-arn', 'Values': [task_arn]}])
        except client.exceptions.ResourceNotFoundFault:
            logging.warning(f"{task_name}: Replication task not found")
            continue

        # Describe table statistics for the given replication task
        validation_details = client.describe_table_statistics(ReplicationTaskArn=task_arn)

        # Initialize flags for missing and duplicate data
        has_missing_data = False
        has_duplicate_data = False

        for table_statistics in validation_details.get('TableStatistics', []):
            schema_name = table_statistics['SchemaName']
            table_name = table_statistics['TableName']
            inserts = table_statistics['Inserts']
            updates = table_statistics['Updates']
            deletes = table_statistics['Deletes']
            applied_inserts = table_statistics['AppliedInserts']
            applied_updates = table_statistics['AppliedUpdates']
            applied_deletes = table_statistics['AppliedDeletes']
            validation_state = table_statistics['ValidationState']

            if validation_state == 'Validated':
                # Check for possible missing data
                if inserts > applied_inserts or updates > applied_updates or deletes < applied_deletes:
                    logging.info(
                        f"Potential missing data in {schema_name}.{table_name}: "
                        f"≠ inserts/applied_inserts: {inserts - applied_inserts}, "
                        f"≠ updates/applied_updates: {updates - applied_updates}, "
                        f"≠ deletes/applied_deletes: {deletes - applied_deletes}"
                    )
                    has_missing_data = True

                # Check for possible duplicate data
                if applied_inserts > inserts or applied_updates > updates or applied_deletes < deletes:
                    logging.info(
                        f"Potential duplicate data in {schema_name}.{table_name}: "
                        f"≠ applied_inserts/inserts: {applied_inserts - inserts}, "
                        f"≠ applied_updates/updates: {applied_updates - updates}, "
                        f"≠ applied_deletes/deletes: {deletes - applied_deletes}"
                    )
                    has_duplicate_data = True

        # Determine event name and status
        if has_missing_data:
            event_name = f"{task_name}_dms_missing"
            status = 0
        elif has_duplicate_data:
            event_name = f"{task_name}_dms_duplicates"
            status = 0
        else:
            event_name = f"{task_name}_dms_no_issues"
            status = 1
            logging.info(f"{task_name}: No missing or duplicate data detected!")

        # Send event notification
        response = requests.post(NOTIFIER_URL, json={'name': event_name, 'status': status})
        
        # Handle HTTP response
        if response.status_code != 200:
            logging.error(f"Failed to send notification for {event_name}. Status code: {response.status_code}")
        else:
            logging.info(f"Notification sent for {event_name} with status {status}")

    return {}

@test
def test_output(output: Dict[str, Any], *args) -> None:
    """Tests the output of the load_data function."""
    assert output is not None, 'The output is undefined'