from main import get_pdf_image, perform_cloud_vision

def test_local():
    local_image = get_pdf_image('test.png', True, '/Users/eriksandberg/Downloads/online-server-test-5be6288e792b.json')
    output_text = perform_cloud_vision(local_image, True, '/Users/eriksandberg/Downloads/online-server-test-5be6288e792b.json')
    print(output_text)

if __name__ == "__main__":
    test_local()