import json, os, logging
import boto3, botocore

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("event: {}".format(event))
    s3 = boto3.client("s3")

    verification_bucket = os.getenv("bucketName")
    verification_answer = "c1ws_log4shell_task3_answer"
    lookup_key = "Reason" # To Ensure that the Reason key exist in the message event.
    event_reason_checker = "1011242" # IPS Log4J Rule Number
    message = event["Records"][0]["Sns"]["Message"]

    dict_message = json.loads(message)
    logger.info(type(dict_message))

    if type(dict_message) is list:
        if lookup_key in dict_message[0]:
            reason = dict_message[0]["Reason"].split(" ")[0]
            if reason == event_reason_checker:
                try:
                    response = s3.put_object(
                        Bucket = verification_bucket,
                        Key    = verification_answer
                    )
                    return {
                        "Response Code" : response["ResponseMetadata"]["HTTPStatusCode"]
                    }
                except botocore.exceptions.ClientError as error:
                    raise error
            else:
                logger.info("Reason Number isn't correct")
        else:
            logger.info("Reason Key doesn't exist")

    elif type(dict_message) is dict:
            if lookup_key in dict_message:
                reason = dict_message["Reason"].split(" ")[0]
                if reason == event_reason_checker:
                    try:
                        response = s3.put_object(
                            Bucket = verification_bucket,
                            Key    = verification_answer
                        )
                        return {
                            "Response Code" : response["ResponseMetadata"]["HTTPStatusCode"]
                        }
                    except botocore.exceptions.ClientError as error:
                        raise error
                else:
                    logger.info("Reason Number isn't correct")
            else:
                logger.info("Reason Key doesn't exist")

    else:
        logger.info("Event is misconfigured")