import json

def lambda_handler(event, context):
        try:

                response_body = {"message":"Hello World"}
   

                return {
                "statusCode": 200,
                "body": json.dumps(response_body)
                }
        
        except (Exception) as error:
                return {
                        'statusCode': 500,
                        'body': json.dumps({'error': str(error)})
                 }