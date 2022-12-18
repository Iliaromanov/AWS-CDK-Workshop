import json

def handler(event, context):
    print("request: ", json.dumps(event))
    return {
        'statusCode': 200,
        'headers': {
            'Context-Type': 'text/plain'
        },
        'body': f"Hello Sofya, you have hit {event['path']}\n"
    }
