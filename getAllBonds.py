import json
import boto3


def lambda_handler(event, context):

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('private-info-gorbenko')
    obj = bucket.Object(key = 'bonds.txt')
    response = obj.get()

    lines = response[u'Body'].read().decode('Windows−1251').splitlines()
    responce_body = []

    if lines:
        headers = lines[0].split("\t")
        print(event)
        print(dir(event))
        print(event['page'])

    try:
        for i in range(1, len(lines)):

            d = dict((u''.join(key), u''.join(value)) for (key, value)
                in zip(headers, lines[i].split("\t")))
            responce_body.append(d)

        return {
            'statusCode': 200,
            'body': responce_body
        }

    except Exception as e:
        return {
            'statusCode': 400,
            'body': 'It seems an ERROR!' + e
        }
