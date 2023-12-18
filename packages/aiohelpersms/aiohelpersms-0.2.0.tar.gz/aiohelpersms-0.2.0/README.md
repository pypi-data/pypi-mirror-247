
## Quickstart
1. Install package `pip install aiohelpersms`
2. Install dependencies `pip install -r aiohelpersms/requirements.txt`
3. See examples
4. Read the [documentation](https://api.helper20sms.ru/docs)

## Usage
1. `from aiohelpersms import AioHelperSMS, BadApiKeyProvidedException`
2. `client = AioHelperSMS('your_api_token')`
3. See example

``` python
balance = await client.get_balance()
print(balance)

countries = await client.get_countries()
print(countries)
```

## Exception handling

``` python
from aiohelpersms import AioHelperSMS, BadApiKeyProvidedException

client = AioHelperSMS(token)
try:
	balance = await client.get_balance()
	print(balance)
except BadApiKeyProvidedException as e:
	print(e)
```
`> {'detail': 'Bad API key provided'}`

See the documentation for exceptions in the ```exceptions.md``` file

## Sync version

``` python
from aiohelpersms import HelperSMS, BadApiKeyProvidedException

token = 'your_api_token'

def main(token):
	client = HelperSMS(token)

	try:
		balance = client.get_balance()
		print(balance)

		countries = client.get_countries()
		print(countries)
	except BadApiKeyProvidedException as e:
		print(e)


if __name__ == '__main__':
    main()
```

## Other

[![Downloads](https://static.pepy.tech/badge/aiohelpersms)](https://pepy.tech/project/aiohelpersms)

## License

Project AioHelperSMS is distributed under the MIT license