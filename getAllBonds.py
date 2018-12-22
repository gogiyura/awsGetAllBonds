import json
import boto3


def lambda_handler(event, context):

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('private-info-gorbenko')
    obj = bucket.Object(key = 'bonds.txt')
    response = obj.get()

    lines = response[u'Body'].read().decode('Windows−1251').splitlines()
    response_body = []

    collection_per_page = 10
    page_count = -(-len(lines) // collection_per_page)

    """ Mandatory parameter is the page """
    if 'page' in event:
        num_page = event['page']
    else:
        return {
            'statusCode': 403,
            'page' : -1,
            'body': "Mandatory parameter 'Page' is missing at the query"
        }

    """ Number of page should be integer """
    if not isinstance(num_page, int):
        return {
            'statusCode': 403,
            'page' : -1,
            'body': "Please, check the parameter 'Number of a page' at the query"
        }

    if num_page > page_count:
        return {
            'statusCode': 403,
            'page' : num_page,
            'body': "The paremeter 'Page' should not be more than " + str(page_count)
        }

    try:
        """ Receiving the headers for columns """
        if lines:
            headers = lines[0].split("\t")

        lines_proc = list(pagination(lines, collection_per_page))[num_page]

        for i in range(0, len(lines_proc)):
            d = dict((u''.join(key), u''.join(value)) for (key, value)
                in zip(headers, lines_proc[i].split("\t")))

            response_body.append(d)

        return {
            'statusCode': 200,
            'page' : num_page,
            'body': response_body
        }

    except Exception as e:
        return {
            'statusCode': 400,
            'page' : -1,
            'body': 'It seems an ERROR!' + e
        }

def pagination(seq, rows_per_page):
    for start in range(1, len(seq), rows_per_page):
        yield seq[start:start + rows_per_page]

if __name__ == '__main__':
    lambda_handler({"page": 0}, '')
