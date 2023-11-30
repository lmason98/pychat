from openai import OpenAI, BadRequestError
from base64 import b64decode
from pathlib import Path

import time
import sys

CLIENT = OpenAI()
IMAGE_DIR = Path.cwd() / "images"
IMAGE_DIR.mkdir(parents=True, exist_ok=True)


def main(args):

	if len(args) < 2:
		print("Please enter a prompt to generate an image.")
		return
	elif len(args) > 2:
		print("Please enter a single prompt to generate an image.")
		return

	prompt = args[1].lower()

	if prompt == "" or prompt.isspace():
		print("Please enter a valid prompt to generate an image.")
		return

	start = time.time()
	try:
		response = CLIENT.images.generate(
			prompt=prompt,
			n=2,
			size="1024x1024",
			response_format="b64_json"
		)
		print(f"Elapsed time : {time.time() - start}")

		image_data = b64decode(response.data[0].b64_json)
		image_file = IMAGE_DIR / f"{prompt[:10]}-{response.created}.png"

		with open(image_file, "wb") as png:
			png.write(image_data)
	except BadRequestError as e:
		print("There was a problem generating your image :", e)


if __name__ == '__main__':
	main(sys.argv)
