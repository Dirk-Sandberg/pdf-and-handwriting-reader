def get_pdf_image(pdf_image_url, local=False, cred_file=''):
    from google.cloud import storage
    if local:
        output_filename = './temp.png'
    else:
        # Cloud Function environment only allows write to /tmp folder
        output_filename = '/tmp/temp.png'
    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    if local:
        storage_client = storage.Client.from_service_account_json(cred_file)
    else:
        storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    bucket = storage_client.get_bucket('oneline-server-test')
    blob = bucket.blob(pdf_image_url)
    blob.download_to_filename(output_filename)
    return output_filename

def perform_cloud_vision(image_filename, local=False, cred_file=''):
    from google.cloud import vision
    from google.cloud.vision import types
    if local:
        client = vision.ImageAnnotatorClient.from_service_account_file(cred_file)
    else:
        # If you don't specify credentials when constructing the client, the
        # client library will look for credentials in the environment.
        client = vision.ImageAnnotatorClient()
    with open(image_filename, 'rb') as f:
        content = f.read()
    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)
    doc_text = response.full_text_annotation.text
    return doc_text


def detect_handwriting(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    local_image = get_pdf_image('test.png')
    output_text = perform_cloud_vision(local_image)

    request_json = request.get_json()
    try:
        print('form requests', request.form)
    except:
        print("couldn't print form")
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return output_text



