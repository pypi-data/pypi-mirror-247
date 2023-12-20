import base64

class ImageHandler:
    @staticmethod
    def encode_image_to_base64(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        return encoded_string

    @staticmethod
    def decode_base64_to_image(encoded_string, output_path):
        with open(output_path, "wb") as image_file:
            image_file.write(base64.b64decode(encoded_string))
