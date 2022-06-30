import boto3.client
import cfnresponse

s3_control_client = boto3.client("s3control")


def remove_access_points(bucket_name: str, account_id: str):
    access_points_raw = s3_control_client.list_access_points(
        AccountId=account_id, Bucket=bucket_name
    ).get("AccessPointList")
    if access_points_raw:
        access_points = [dict.get("Name") for dict in access_points_raw]
        print(access_points)
        for access_point in access_points:
            try:
                response = s3_control_client.delete_access_point(
                    AccountId=account_id, Name=access_point
                )
            except Exception as e:
                print(f"Exception is: {e}")


def handler(event, context):
    # Init ...
    the_event = event["RequestType"]
    print("The event is: ", str(the_event))
    response_data = {}
    # Retrieve parameters
    the_bucket = event["ResourceProperties"]["the_bucket"]
    try:
        if the_event == "Delete":
            print("Deleting S3 content...")
            b_operator = boto3.resource("s3")
            b_operator.Bucket(str(the_bucket)).objects.all().delete()

            print("Removing access points...")
            b_operator = boto3.resource("s3")
            remove_access_points(str(the_bucket), "${AWS::AccountId}")
        # Everything OK... send the signal back
        print("Operation successful!")
        cfnresponse.send(event, context, cfnresponse.SUCCESS, response_data)
    except Exception as e:
        print("Operation failed...")
        print(str(e))
        response_data["Data"] = str(e)
        cfnresponse.send(event, context, cfnresponse.FAILED, response_data)
