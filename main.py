from kivy.app import App
from kivy.network.urlrequest import UrlRequest
import certifi


class MainApp(App):
    source_file_name = 'temp.jpg'

    def take_image(self):
        from plyer import camera
        filepath = self.user_data_dir + '/' + 'temp.png'
        try:
            camera.take_picture(filename=filepath,
                            on_complete=self.camera_callback)
        except NotImplementedError:
            print("Can't take a picture on this platform")

    def camera_callback(self, filepath):
        from os.path import exists
        if(exists(filepath)):
            print("Picture saved!", filepath)
            self.source_file_name = filepath
            self.upload_image()
        else:
            print("Couldnt save picture")


    def detect_handwriting(self):
        print("Detecting handwriting...")
        blob_name = self.select_image()

    def select_image(self):
        # Select a file from your device
        self.take_image()
        self.root.ids.message_label.text = 'Uploading image...'
        # Upload the file

    def upload_image(self):
        from google.cloud import storage

        """Uploads a file to the bucket."""
        bucket_name = 'oneline-server-test'
        destination_blob_name = "test-storage-blob.png"
        debug = True
        if not debug:
            storage_client = storage.Client()
        else:
            cred_file = 'online-server-test-5be6288e792b.json'
            storage_client = storage.Client.from_service_account_json(cred_file)

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(self.source_file_name)
        print(
            "File {} uploaded to {}.".format(
                self.source_file_name, destination_blob_name
            )
        )

        self.hit_cloud_function(destination_blob_name)

    def hit_cloud_function(self, blob_name):
        self.root.ids.message_label.text = 'Identifying text...'
        from urllib.parse import urlencode
        msg_data = urlencode({'message': blob_name})
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/plain'}

        print("Sending trigger request")
        trigger_url = "https://us-central1-online-server-test.cloudfunctions.net/detect-handwriting"
        UrlRequest(trigger_url, req_body=msg_data, req_headers=headers, ca_file=certifi.where(),
                   on_failure=self.error, on_error=self.error, on_success=self.success)

    def error(self, *args):
        print("Error", args)

    def success(self, request, response):
        print("Success!")
        print(response)
        self.root.ids.message_label.text = response


MainApp().run()
