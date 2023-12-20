
## Quickstart
1. Install package `pip install helper20sms`
2. See examples
3. Read the [documentation](https://api.helper20sms.ru/docs)

## Usage
1. `from helper20sms import AioHelper20SMS, BadApiKeyProvidedException`
2. `client = AioHelper20SMS('your_api_token')`
3. See example

``` python
balance = await client.get_balance()
print(balance)

countries = await client.get_countries()
print(countries)
```

## Exception handling

``` python
from aiohelper20sms import AioHelper20SMS, BadApiKeyProvidedException

client = AioHelper20SMS(token)
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
from aiohelper20sms import Helper20SMS, BadApiKeyProvidedException

token = 'your_api_token'

def main(token):
	client = Helper20SMS(token)

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

[![Downloads](https://static.pepy.tech/badge/helper20sms)](https://pepy.tech/project/helper20sms)

## License

Project AioHelperSMS is distributed under the MIT license
