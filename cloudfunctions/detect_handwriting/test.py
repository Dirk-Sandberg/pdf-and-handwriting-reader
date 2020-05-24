from main import get_pdf_image

def test_local():
    get_pdf_image('test.png', True, '/Users/eriksandberg/Downloads/online-server-test-5be6288e792b.json')

if __name__ == "__main__":
    test_local()