import json, os, logging
import boto3, botocore

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("event: {}".format(event))
    s3 = boto3.client("s3")

    verification_bucket = os.getenv("bucketName")
    verification_answer = "c1ws_log4shell_task2_answer"
    lookup_key          = "Contents"
    result_flag         = False

    try:
        response = s3.list_objects_v2(
        Bucket=verification_bucket
    )
        if lookup_key in response:
            logger.info(response["Contents"])
            for object in response["Contents"]:
                if object["Key"] == verification_answer:
                    result_flag = True
                    break

            # Return task result
            if result_flag == False:
                raise Exception("Log Inspection event isn't in the Cloud One Console yet.")
                return result_flag
        
            return result_flag
            
        else:
            raise Exception("Log Inspection event isn't in the Cloud One Console yet.")
            return result_flag

    except botocore.exceptions.ClientError as error:
        raise error