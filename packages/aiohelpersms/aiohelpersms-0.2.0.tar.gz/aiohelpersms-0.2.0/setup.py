from setuptools import setup
from io import open


def read(filename):
   """Прочитаем наш README.md для того, чтобы установить большое описание."""
   with open(filename, "r", encoding="utf-8") as file:
      return file.read()

setup(
	name="aiohelpersms",
	version='0.2.0',
	long_description=read("README.md"),
	long_description_content_type="text/markdown",
	url="https://github.com/fantomcvc/aiohelpersms",
	license="MIT License",
	author="fantomcvc",
	author_email='fantomcvv@gmail.com',
	description="Async API wrapper for helpersms ",
	packages=['aiohelpersms'],
)
