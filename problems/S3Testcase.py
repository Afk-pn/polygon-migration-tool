import logging
import boto3

logger = logging.getLogger(__name__)


class S3TestcaseManager:
    """
    Uploads Polygon test cases to Amazon S3.

    Objects are stored as:
        test_cases/{db_problem_id}/{test_number}
        test_cases/{db_problem_id}/{test_number}.a
    """

    def __init__(self, bucket_name, region_name=None):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            "s3",
            region_name=region_name
        )

    def upload_test_case(
        self,
        container_name,
        db_problem_id,
        test_number,
        input_data,
        output_data
    ):
        input_key = f"test_cases/{db_problem_id}/{test_number:02d}"
        output_key = f"test_cases/{db_problem_id}/{test_number:02d}.a"

        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=input_key,
            Body=input_data.encode("utf-8")
        )

        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=output_key,
            Body=output_data.encode("utf-8")
        )

        logger.info(
            "Uploaded test #%s to s3://%s/%s",
            test_number,
            self.bucket_name,
            input_key
        )

    def empty_blob(self, container_name, problem_id):
        prefix = f"test_cases/{problem_id}/"

        response = self.s3_client.list_objects_v2(
            Bucket=self.bucket_name,
            Prefix=prefix
        )

        objects = response.get("Contents", [])

        if objects:
            self.s3_client.delete_objects(
                Bucket=self.bucket_name,
                Delete={
                    "Objects": [
                        {"Key": obj["Key"]}
                        for obj in objects
                    ]
                }
            )

        logger.info(
            "Deleted %s existing objects for problem %s",
            len(objects),
            problem_id
        )