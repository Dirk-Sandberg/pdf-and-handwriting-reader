from kivy.app import App
from kivy.network.urlrequest import UrlRequest


class MainApp(App):
    def detect_handwriting(self):
        print("Detecting handwriting...")
        blob_name = self.select_image()
        self.hit_cloud_function(blob_name)

    def select_image(self):
        # Select a file from your device
        source_file_name = 'temp.jpg'
        # Upload the file

        from google.cloud import storage

        """Uploads a file to the bucket."""
        bucket_name = 'oneline-server-test'
        destination_blob_name = "test-storage-blob.png"
        debug = True
        if not debug:
            storage_client = storage.Client()
        else:
            cred_file = '/Users/eriksandberg/Downloads/online-server-test-5be6288e792b.json'
            storage_client = storage.Client.from_service_account_json(cred_file)

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)
        print(
            "File {} uploaded to {}.".format(
                source_file_name, destination_blob_name
            )
        )
        return destination_blob_name

    def hit_cloud_function(self, blob_name):
        from urllib.parse import urlencode
        msg_data = urlencode({'message': blob_name})
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/plain'}

        print("Sending trigger request")
        trigger_url = "https://us-central1-online-server-test.cloudfunctions.net/detect-handwriting"
        UrlRequest(trigger_url, req_body=msg_data, req_headers=headers,
                   on_failure=self.error, on_error=self.error, on_success=self.success)

    def error(self, *args):
        print("Error", args)

    def success(self, request, response):
        print("Success!")
        print(response)

MainApp().run()