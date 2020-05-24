def get_pdf_image(pdf_image_url, local=False, cred_file=''):
    from google.cloud import storage
    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    if local:
        storage_client = storage.Client.from_service_account_json(cred_file)
    else:
        storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)
    bucket = storage_client.get_bucket('oneline-server-test')
    blob = bucket.blob(pdf_image_url)
    blob.download_to_filename('./temp.png')

    print('ay', bucket)


def detect_handwriting(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    get_pdf_image()
    request_json = request.get_json()
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return f'Hello World!'



