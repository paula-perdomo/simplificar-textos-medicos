import boto3
from botocore.exceptions import ClientError
import os
from fastapi import HTTPException


def get_secret(secret_name):
    region_name =  os.environ['AWS_REGION']

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret " + secret_name + " was not found")
            raise HTTPException(status_code=404, detail="Secret not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("The request was invalid due to:", e)
            raise HTTPException(status_code=400, detail="Invalid request")
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", e)
            raise HTTPException(status_code=400, detail="Invalid parameters")
        elif e.response['Error']['Code'] == 'DecryptionFailure':
            print("The requested secret can't be decrypted using the provided KMS key:", e)
            raise HTTPException(status_code=400, detail="Decryption failure")
        elif e.response['Error']['Code'] == 'InternalServiceError':
            print("An error occurred on service side:", e)
            raise HTTPException(status_code=500, detail="Internal service error")

    else:
        # Secrets Manager decrypts the secret value using the associated KMS CMK
        # Depending on whether the secret was a string or binary, only one of these fields will be populated
        print(get_secret_value_response)
        
        return get_secret_value_response['SecretString']
       