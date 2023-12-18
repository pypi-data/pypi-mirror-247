import asyncio
import aiohttp
import platform

from typing import Dict, Optional, List

import requests


if platform.system() == "Windows":
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class OtherApiException(Exception):
	pass

class ValidationException(Exception):
	pass

class NoApiKeyProvidedException(Exception):
	pass

class BadApiKeyProvidedException(Exception):
	pass

class ForbiddenAccessException(Exception):
	pass

class BadCountryIdException(Exception):
	pass

class BadServiceIdException(Exception):
	pass

class WrongOperatorCodeException(Exception):
	pass

class InternalErrorException(Exception):
	pass

class NoNumbersException(Exception):
	pass

class BlockedUserException(Exception):
	pass

class InsufficientFundsException(Exception):
	pass

class CannotBuyMailRuServicesException(Exception):
	pass

class NoNumbersWithMaxPriceException(Exception):
	pass

class TooFastOperationException(Exception):
	pass

class OrderStatusChangeException(Exception):
	pass

class TooEarlyCancellationException(Exception):
	pass

class OrderProcessingException(Exception):
	pass

class UnsupportedOrderTypeException(Exception):
	pass

class TechnicalWorksException(Exception):
	pass

class RentTimeNotAvailableException(Exception):
	pass

class InvalidServiceCountException(Exception):
	pass




class AioHelperSMS:
	path_prefix = "https://api.helper20sms.ru"


	def __init__(self, api_key: str) -> None:
		"""__init__
		Args:
			api_key (str): HelperSMS api key
		"""
		
		self.__headers = {
			"api-key": api_key,
		}
	
	
	async def get_balance(self) -> Dict:
		"""Получить информацию о балансе
		Returns:
			Dict: {
				"status": true,
				"data":
				{
					"balance": 20.22
				}
			}
		"""
		method = "GET"
		path = "/api/balance"
		return await self._request(method, path)


	async def get_countries(self) -> Dict:
		"""Получить список стран
		Returns:
			Dict: {
				"status": true,
				"data":
				[
					{
						"id": 1,
						"name": "Россия"
					}
				]
			}
		"""
		method = "GET"
		path = "/api/countries"
		return await self._request(method, path)


	async def get_services(self, country_id: int):
		"""Получить список сервисов определённой страны
		Args:
			country_id (int): Айди страны
		Returns:
			Dict: {
				"status": true,
				"data":
				[
					{
						"id": 6104,
						"name": "Вконтакте"
					}
				]
			}
		"""
		if not isinstance(country_id, int):
			raise ValidationException("Argument country_id must be an integer")

		method = "GET"
		path = f"/api/services/{country_id}"
		return await self._request(method, path)


	async def get_operators(self, country_id: int):
		"""Получить список операторов определённой страны
		Args:
			country_id (int): Айди страны
		Returns:
			Dict: {
				"status": true,
				"data":
				[
					"mtt",
					"megafon",
					"beeline"
				]
			}
		"""
		if not isinstance(country_id, int):
			raise ValidationException("Argument country_id must be an integer")

		method = "GET"
		path = f"/api/operators/{country_id}"
		return await self._request(method, path)

	
	async def get_price(
		self,
		service_id: int,
		reorder_ability: Optional[bool] = False,
	) -> Dict:
		"""Получить цену СМС для сервиса
		Args:
			service_id (int): Айди сервиса
			reorder_ability (Optional[bool], optional): Возможность повторной покупки номера после конца аренды. Default value: false
		Returns:
			Dict: {
				"status": true,
				"data":
				{
					"price": 20.04,
					"service": "vk"
				}
			}
		"""
		if not isinstance(service_id, int):
			raise ValidationException("Argument service_id must be an integer")
		if not isinstance(reorder_ability, bool):
			raise ValidationException("Argument reorder_ability must be an boolean")

		method = "GET"
		path = f"/api/price/{service_id}"
		data = {
			'reorder_ability': reorder_ability
		}

		for key, value in data.copy().items():
			if value is None:
				del data[key]
		
		return await self._request(method, path, data)



	async def get_number(
		self,
		service_id: int,
		operator_code: Optional[str] = 'any',
		reorder_ability: Optional[bool] = False,
		max_price: Optional[int] = 0,
		in_bot_notifications: Optional[bool] = False,
	) -> Dict:
		"""Купить номер для получения СМС
		Args:
			service_id (int): Айди сервиса
			operator_code: (Optional[str], optional): Код оператора. Default value: any
			reorder_ability (Optional[bool], optional): Возможность повторной покупки номера после конца аренды. Default value: false
			max_price (Optional[int], optional): Максимальная цена. Default value: 0
			in_bot_notifications (Optional[bool, optional]): Уведомление внутри бота. Default value: false
		Returns:
			Dict: {
				"status": true,
				"data":
				{
					"order_id": 1,
					"number": "79851478547",
					"service": "vk",
					"price": 20.22
				}
			}
		"""
		if not isinstance(service_id, int):
			raise ValidationException("Argument service_id must be an integer")
		if not isinstance(operator_code, str):
			raise ValidationException("Argument operator_code must be an string")
		if not isinstance(reorder_ability, bool):
			raise ValidationException("Argument reorder_ability must be an boolean")
		if not isinstance(max_price, int):
			raise ValidationException("Argument max_price must be an integer")
		if not isinstance(in_bot_notifications, bool):
			raise ValidationException("Argument in_bot_notifications must be an boolean")

		method = "POST"
		path = "/api/number"
		data = {
			'service_id': service_id,
			'operator_code': operator_code,
			'reorder_ability': reorder_ability,
			'max_price': max_price,
			'in_bot_notifications': in_bot_notifications
		}
		for key, value in data.copy().items():
			if value is None:
				del data[key]
		
		return await self._request(method, path, data)


	
	async def set_order_status(
		self,
		order_id: int,
		status: str
	) -> Dict:
		"""Изменить статус для заказа
		Args:
			order_id (int): Номер заказа
			status: (str): Статус заказа. Допустимые значения: CANCEL, FINISH
		Returns:
			Dict: {
				"status": true
			}
		"""
		if not isinstance(order_id, int):
			raise ValidationException("Argument order_id must be an integer")
		if not isinstance(status, str):
			raise ValidationException("Argument status must be an string")

		method = "POST"
		path = "/api/order_status"
		data = {
			'order_id': order_id,
			'status': status,
		}
		for key, value in data.copy().items():
			if value is None:
				del data[key]

		return await self._request(method, path, data)



	async def get_codes(
		self,
		order_id: int,
	) -> Dict:
		"""Получить список полученных кодов для номера
		Args:
			order_id (int): Номер заказа
		Returns:
			Dict: {
				"status": true,
				"data":
				{
					"codes":
					[
						"5423",
						"125423",
						"4158"
					]
				}
			}
		"""
		if not isinstance(order_id, int):
			raise ValidationException("Argument order_id must be an integer")

		method = "GET"
		path = f"/api/codes/{order_id}"

		return await self._request(method, path)
	


	async def get_rent_services(
		self,
		country_id: int,
	) -> Dict:
		"""Получить список сервисов для аренды определённой страны
		Args:
			country_id (int): Айди страны
		Returns:
			Dict: {
				"status": true,
				"data":
				[
					{
						"id": 1,
						"name": "Alibaba"
					}
				]
			}
		"""
		if not isinstance(country_id, int):
			raise ValidationException("Argument country_id must be an integer")

		method = "GET"
		path = f"/api/rent_services/{country_id}"

		return await self._request(method, path)



	async def get_rent_price(
		self,
		service_id : int,
		rent_time: int,
	) -> Dict:
		"""Получить цену аренды для сервиса
		Args:
			service_id (int): Айди сервиса
			rent_time (int): Период аренды номера. Минимум 4 часа
		Returns:
			Dict: {
				"status": true,
				"data":
				{
					"price": 20.04,
					"service": "vk"
				}
			}
		"""
		if not isinstance(service_id, int):
			raise ValidationException("Argument service_id must be an integer")
		if not isinstance(rent_time, int):
			raise ValidationException("Argument rent_time must be an integer")

		method = "GET"
		path = f"/api/rent_price/{service_id}/{rent_time}"

		return await self._request(method, path)



	async def get_rent_number(
		self,
		service_id : int,
		rent_time: int,
		operator_code: Optional[str] = 'any',
	) -> Dict:
		"""Купить номер для аренды
		Args:
			service_id (int): Айди сервиса
			rent_time (int): Период аренды номера. Минимум 4 часа
			operator_code: (Optional[str], optional): Код оператора. Default value: any
		Returns:
			Dict: {
				"status": true,
				"data":
				{
					"order_id": 1,
					"number": "79851478547",
					"service": "vk",
					"price": 20.22
				}
			}
		"""
		if not isinstance(service_id, int):
			raise ValidationException("Argument service_id must be an integer")
		if not isinstance(rent_time, int):
			raise ValidationException("Argument rent_time must be an integer")
		if not isinstance(operator_code, str):
			raise ValidationException("Argument operator_code must be an string")

		method = "POST"
		path = "/api/rent_number"
		data = {
			'service_id': service_id,
			'rent_time': rent_time,
			'operator_code': operator_code,
		}
		for key, value in data.copy().items():
			if value is None:
				del data[key]

		return await self._request(method, path, data)

	async def get_multiservice(
		self,
		country_id : int,
	) -> Dict:
		"""Получить список сервисов мультисервиса
		Args:
			country_id (int): Айди страны
		Returns:
			Dict: {
				"status": true,
				"data": [
					{
					"id": 6104,
					"name": "Вконтакте"
					}
				]
			}
		"""
		if not isinstance(country_id, int):
			raise ValidationException("Argument service_id must be an integer")

		method = "GET"
		path = f"/api/multiservice/services/{country_id}"

		return await self._request(method, path)
	
	async def get_multiservice_price(
		self,
		service_id: List[int],
		operator_code: Optional[str] = 'any',
	) -> Dict:
		"""Получить цену номера для нескольких сервисов
		Args:
			service_id List(int): ID сервисов
			operator_code: (Optional[str], optional): Код оператора. Default value: any
		Returns:
			Dict: {
				"status": true,
				"data": {
					"price": 20.04,
					"count": 1000,
					"service": "vk"
				}
			}
		"""
		if not isinstance(service_id, list) or not all(isinstance(item, int) for item in service_id):
			raise ValidationException("Argument service_id must be a list of integers")
		if not isinstance(operator_code, str):
			raise ValidationException("Argument operator_code must be an string")


		method = "GET"
		path = f"/api/multiservice/price"
		data = {
			'service_id': service_id,
			'operator_code': operator_code,
		}
		for key, value in data.copy().items():
			if value is None:
				del data[key]
		
		return await self._request(method, path, data)
	
	async def get_multiservice_number(
		self,
		services_ids: List[int],
		operator_code: Optional[str] = 'any',
	) -> Dict:
		"""Купить номер для нескольких сервисов
		Args:
			services_ids List(int): ID сервисов
			operator_code: (Optional[str], optional): Код оператора. Default value: any
		Returns:
			Dict: {
				"status": true,
				"data": {
					"order_id": 1,
					"number": "79851478547",
					"service": "vk",
					"price": 20.22
				}
			}
		"""
		if not isinstance(services_ids, list) or not all(isinstance(item, int) for item in services_ids):
			raise ValidationException("Argument service_id must be a list of integers")
		if not isinstance(operator_code, str):
			raise ValidationException("Argument operator_code must be an string")

		method = "POST"
		path = "/api/multiservice/number"
		data = {
			'services_ids': services_ids,
			'operator_code': operator_code,
		}
		for key, value in data.copy().items():
			if value is None:
				del data[key]

		return await self._request(method, path, data)
	
	async def get_multiservice_codes(
		self,
		order_id: int,
	) -> Dict:
		"""Получить список полученных кодов для номера
		Args:
			order_id int: ID заказа
		Returns:
			Dict: {
				"status": true,
				"data": {
					"codes": {
					"100": [
						"5423",
						"125423",
						"4158"
					],
					"113": [
						"3654",
						"148741",
						"3574"
					]
					}
				}
			}
		"""
		if not isinstance(order_id, str):
			raise ValidationException("Argument order_id must be an integer")


		method = "GET"
		path = f"/api/multiservice/codes/{order_id}"
		
		return await self._request(method, path)
	
	
	async def _request(self, method: str, path: str, data: dict = {}) -> Dict:
		url = self.path_prefix + path	

		async with aiohttp.ClientSession() as session:
			async with session.request(
				method, url, headers=self.__headers, json=data
			) as response:
				result = await response.json()
				if isinstance(result, dict) and 'detail' in result:
					if result['detail'] == 'No API key provided':
						raise NoApiKeyProvidedException(result)
					elif result["detail"] == 'Bad API key provided':
						raise BadApiKeyProvidedException(result)
					elif result["detail"] == 'Forbidden':
						raise ForbiddenAccessException(result)
					elif result["detail"] == 'Bad country_id provided':
						raise BadCountryIdException(result)
					elif result["detail"] == 'Bad service_id provided':
						raise BadServiceIdException(result)
					elif result["detail"] == 'Wrong operator code':
						raise WrongOperatorCodeException(result)
					elif result["detail"] == 'Internal error' or result["detail"] == 'Please, contact tech support' or 'Error due number ordering' in result["detail"]:
						raise InternalErrorException(result)
					elif result["detail"] == 'No numbers':
						raise NoNumbersException(result)
					elif result["detail"] == 'You are blocked':
						raise BlockedUserException(result)
					elif result["detail"] == 'No enough founds on the balance':
						raise InsufficientFundsException(result)
					elif result["detail"] == 'You cannot buy MailRU services':
						raise CannotBuyMailRuServicesException(result)
					elif 'No numbers with current max_price' in result["detail"]:
						raise NoNumbersWithMaxPriceException(result)
					elif 'Too fast, wait' in result["detail"]:
						raise TooFastOperationException(result)
					elif 'finish this order' in result["detail"]:
						raise OrderStatusChangeException(result)
					elif 'Too early, cancel is available after' in result["detail"]:
						raise TooEarlyCancellationException(result)
					elif 'Error during' in result["detail"]:
						raise OrderProcessingException(result)
					elif 'Unsupported order type' in result["detail"]:
						raise UnsupportedOrderTypeException(result)
					elif result["detail"] == 'Technical works, please try again later':
						raise TechnicalWorksException(result)
					elif result["detail"] == 'Not available with this rent_time':
						raise RentTimeNotAvailableException(result)
					elif result["detail"] == 'Minimum 2 services, maximum 5 services':
						raise InvalidServiceCountException(result)
					else:
						raise OtherApiException(result)
				else:
					return result


class HelperSMS:
	path_prefix = "https://api.helper20sms.ru"


	def __init__(self, api_key: str) -> None:
		"""__init__
		Args:
			api_key (str): HelperSMS api key
		"""
		
		self.__headers = {
			"api-key": api_key,
		}
	
	
	def get_balance(self) -> Dict:
		"""Получить информацию о балансе
		Returns:
			Dict: {
				"status": true,
				"data":
				{
					"balance": 20.22
				}
			}
		"""
		method = "GET"
		path = "/api/balance"
		return self._request(method, path)


	def get_countries(self) -> Dict:
		"""Получить список стран
		Returns:
			Dict: {
				"status": true,
				"data":
				[
					{
						"id": 1,
						"name": "Россия"
					}
				]
			}
		"""
		method = "GET"
		path = "/api/countries"
		return self._request(method, path)


	def get_services(self, country_id: int):
		"""Получить список сервисов определённой страны
		Args:
			country_id (int): Айди страны
		Returns:
			Dict: {
				"status": true,
				"data":
				[
					{
						"id": 6104,
						"name": "Вконтакте"
					}
				]
			}
		"""
		if not isinstance(country_id, int):
			raise ValidationException("Argument country_id must be an integer")

		method = "GET"
		path = f"/api/services/{country_id}"
		return self._request(method, path)


	def get_operators(self, country_id: int):
		"""Получить список операторов определённой страны
		Args:
			country_id (int): Айди страны
		Returns:
			Dict: {
				"status": true,
				"data":
				[
					"mtt",
					"megafon",
					"beeline"
				]
			}
		"""
		if not isinstance(country_id, int):
			raise ValidationException("Argument country_id must be an integer")

		method = "GET"
		path = f"/api/operators/{country_id}"
		return self._request(method, path)

	
	def get_price(
		self,
		service_id: int,
		reorder_ability: Optional[bool] = False,
	) -> Dict:
		"""Получить цену СМС для сервиса
		Args:
			service_id (int): Айди сервиса
			reorder_ability (Optional[bool], optional): Возможность повторной покупки номера после конца аренды. Default value: false
		Returns:
			Dict: {
				"status": true,
				"data":
				{
					"price": 20.04,
					"service": "vk"
				}
			}
		"""
		if not isinstance(service_id, int):
			raise ValidationException("Argument service_id must be an integer")
		if not isinstance(reorder_ability, bool):
			raise ValidationException("Argument reorder_ability must be an boolean")

		method = "GET"
		path = f"/api/price/{service_id}"
		data = {
			'reorder_ability': reorder_ability
		}

		for key, value in data.copy().items():
			if value is None:
				del data[key]
		
		return self._request(method, path, data)



	def get_number(
		self,
		service_id: int,
		operator_code: Optional[str] = 'any',
		reorder_ability: Optional[bool] = False,
		max_price: Optional[int] = 0,
		in_bot_notifications: Optional[bool] = False,
	) -> Dict:
		"""Купить номер для получения СМС
		Args:
			service_id (int): Айди сервиса
			operator_code: (Optional[str], optional): Код оператора. Default value: any
			reorder_ability (Optional[bool], optional): Возможность повторной покупки номера после конца аренды. Default value: false
			max_price (Optional[int], optional): Максимальная цена. Default value: 0
			in_bot_notifications (Optional[bool, optional]): Уведомление внутри бота. Default value: false
		Returns:
			Dict: {
				"status": true,
				"data":
				{
					"order_id": 1,
					"number": "79851478547",
					"service": "vk",
					"price": 20.22
				}
			}
		"""
		if not isinstance(service_id, int):
			raise ValidationException("Argument service_id must be an integer")
		if not isinstance(operator_code, str):
			raise ValidationException("Argument operator_code must be an string")
		if not isinstance(reorder_ability, bool):
			raise ValidationException("Argument reorder_ability must be an boolean")
		if not isinstance(max_price, int):
			raise ValidationException("Argument max_price must be an integer")
		if not isinstance(in_bot_notifications, bool):
			raise ValidationException("Argument in_bot_notifications must be an boolean")

		method = "POST"
		path = "/api/number"
		data = {
			'service_id': service_id,
			'operator_code': operator_code,
			'reorder_ability': reorder_ability,
			'max_price': max_price,
			'in_bot_notifications': in_bot_notifications
		}
		for key, value in data.copy().items():
			if value is None:
				del data[key]
		
		return self._request(method, path, data)


	
	def set_order_status(
		self,
		order_id: int,
		status: str
	) -> Dict:
		"""Изменить статус для заказа
		Args:
			order_id (int): Номер заказа
			status: (str): Статус заказа. Допустимые значения: CANCEL, FINISH
		Returns:
			Dict: {
				"status": true
			}
		"""
		if not isinstance(order_id, int):
			raise ValidationException("Argument order_id must be an integer")
		if not isinstance(status, str):
			raise ValidationException("Argument status must be an string")

		method = "POST"
		path = "/api/order_status"
		data = {
			'order_id': order_id,
			'status': status,
		}
		for key, value in data.copy().items():
			if value is None:
				del data[key]

		return self._request(method, path, data)



	def get_codes(
		self,
		order_id: int,
	) -> Dict:
		"""Получить список полученных кодов для номера
		Args:
			order_id (int): Номер заказа
		Returns:
			Dict: {
				"status": true,
				"data":
				{
					"codes":
					[
						"5423",
						"125423",
						"4158"
					]
				}
			}
		"""
		if not isinstance(order_id, int):
			raise ValidationException("Argument order_id must be an integer")

		method = "GET"
		path = f"/api/codes/{order_id}"

		return self._request(method, path)
	


	def get_rent_services(
		self,
		country_id: int,
	) -> Dict:
		"""Получить список сервисов для аренды определённой страны
		Args:
			country_id (int): Айди страны
		Returns:
			Dict: {
				"status": true,
				"data":
				[
					{
						"id": 1,
						"name": "Alibaba"
					}
				]
			}
		"""
		if not isinstance(country_id, int):
			raise ValidationException("Argument country_id must be an integer")

		method = "GET"
		path = f"/api/rent_services/{country_id}"

		return self._request(method, path)



	def get_rent_price(
		self,
		service_id : int,
		rent_time: int,
	) -> Dict:
		"""Получить цену аренды для сервиса
		Args:
			service_id (int): Айди сервиса
			rent_time (int): Период аренды номера. Минимум 4 часа
		Returns:
			Dict: {
				"status": true,
				"data":
				{
					"price": 20.04,
					"service": "vk"
				}
			}
		"""
		if not isinstance(service_id, int):
			raise ValidationException("Argument service_id must be an integer")
		if not isinstance(rent_time, int):
			raise ValidationException("Argument rent_time must be an integer")

		method = "GET"
		path = f"/api/rent_price/{service_id}/{rent_time}"

		return self._request(method, path)



	def get_rent_number(
		self,
		service_id : int,
		rent_time: int,
		operator_code: Optional[str] = 'any',
	) -> Dict:
		"""Купить номер для аренды
		Args:
			service_id (int): Айди сервиса
			rent_time (int): Период аренды номера. Минимум 4 часа
			operator_code: (Optional[str], optional): Код оператора. Default value: any
		Returns:
			Dict: {
				"status": true,
				"data":
				{
					"order_id": 1,
					"number": "79851478547",
					"service": "vk",
					"price": 20.22
				}
			}
		"""
		if not isinstance(service_id, int):
			raise ValidationException("Argument service_id must be an integer")
		if not isinstance(rent_time, int):
			raise ValidationException("Argument rent_time must be an integer")
		if not isinstance(operator_code, str):
			raise ValidationException("Argument operator_code must be an string")

		method = "POST"
		path = "/api/rent_number"
		data = {
			'service_id': service_id,
			'rent_time': rent_time,
			'operator_code': operator_code,
		}
		for key, value in data.copy().items():
			if value is None:
				del data[key]

		return self._request(method, path, data)

	def get_multiservice(
		self,
		country_id : int,
	) -> Dict:
		"""Получить список сервисов мультисервиса
		Args:
			country_id (int): Айди страны
		Returns:
			Dict: {
				"status": true,
				"data": [
					{
					"id": 6104,
					"name": "Вконтакте"
					}
				]
			}
		"""
		if not isinstance(country_id, int):
			raise ValidationException("Argument service_id must be an integer")

		method = "GET"
		path = f"/api/multiservice/services/{country_id}"

		return self._request(method, path)
	
	def get_multiservice_price(
		self,
		service_id: List[int],
		operator_code: Optional[str] = 'any',
	) -> Dict:
		"""Получить цену номера для нескольких сервисов
		Args:
			service_id List(int): ID сервисов
			operator_code: (Optional[str], optional): Код оператора. Default value: any
		Returns:
			Dict: {
				"status": true,
				"data": {
					"price": 20.04,
					"count": 1000,
					"service": "vk"
				}
			}
		"""
		if not isinstance(service_id, list) or not all(isinstance(item, int) for item in service_id):
			raise ValidationException("Argument service_id must be a list of integers")
		if not isinstance(operator_code, str):
			raise ValidationException("Argument operator_code must be an string")


		method = "GET"
		path = f"/api/multiservice/price"
		data = {
			'service_id': service_id,
			'operator_code': operator_code,
		}
		for key, value in data.copy().items():
			if value is None:
				del data[key]
		
		return self._request(method, path, data)
	
	def get_multiservice_number(
		self,
		services_ids: List[int],
		operator_code: Optional[str] = 'any',
	) -> Dict:
		"""Купить номер для нескольких сервисов
		Args:
			services_ids List(int): ID сервисов
			operator_code: (Optional[str], optional): Код оператора. Default value: any
		Returns:
			Dict: {
				"status": true,
				"data": {
					"order_id": 1,
					"number": "79851478547",
					"service": "vk",
					"price": 20.22
				}
			}
		"""
		if not isinstance(services_ids, list) or not all(isinstance(item, int) for item in services_ids):
			raise ValidationException("Argument service_id must be a list of integers")
		if not isinstance(operator_code, str):
			raise ValidationException("Argument operator_code must be an string")

		method = "POST"
		path = "/api/multiservice/number"
		data = {
			'services_ids': services_ids,
			'operator_code': operator_code,
		}
		for key, value in data.copy().items():
			if value is None:
				del data[key]

		return self._request(method, path, data)
	
	def get_multiservice_codes(
		self,
		order_id: int,
	) -> Dict:
		"""Получить список полученных кодов для номера
		Args:
			order_id int: ID заказа
		Returns:
			Dict: {
				"status": true,
				"data": {
					"codes": {
					"100": [
						"5423",
						"125423",
						"4158"
					],
					"113": [
						"3654",
						"148741",
						"3574"
					]
					}
				}
			}
		"""
		if not isinstance(order_id, str):
			raise ValidationException("Argument order_id must be an integer")


		method = "GET"
		path = f"/api/multiservice/codes/{order_id}"
		
		return self._request(method, path)
	
	
	def _request(self, method: str, path: str, data: dict = {}) -> Dict:
		url = self.path_prefix + path	
		
		if method == 'GET':
			response = requests.get(url, headers=self.__headers, json=data)
		else:
			response = requests.post(url, headers=self.__headers, json=data)
		
		result = response.json()
		if isinstance(result, dict) and 'detail' in result:
			if result['detail'] == 'No API key provided':
				raise NoApiKeyProvidedException(result)
			elif result["detail"] == 'Bad API key provided':
				raise BadApiKeyProvidedException(result)
			elif result["detail"] == 'Forbidden':
				raise ForbiddenAccessException(result)
			elif result["detail"] == 'Bad country_id provided':
				raise BadCountryIdException(result)
			elif result["detail"] == 'Bad service_id provided':
				raise BadServiceIdException(result)
			elif result["detail"] == 'Wrong operator code':
				raise WrongOperatorCodeException(result)
			elif result["detail"] == 'Internal error' or result["detail"] == 'Please, contact tech support' or 'Error due number ordering' in result["detail"]:
				raise InternalErrorException(result)
			elif result["detail"] == 'No numbers':
				raise NoNumbersException(result)
			elif result["detail"] == 'You are blocked':
				raise BlockedUserException(result)
			elif result["detail"] == 'No enough founds on the balance':
				raise InsufficientFundsException(result)
			elif result["detail"] == 'You cannot buy MailRU services':
				raise CannotBuyMailRuServicesException(result)
			elif 'No numbers with current max_price' in result["detail"]:
				raise NoNumbersWithMaxPriceException(result)
			elif 'Too fast, wait' in result["detail"]:
				raise TooFastOperationException(result)
			elif 'finish this order' in result["detail"]:
				raise OrderStatusChangeException(result)
			elif 'Too early, cancel is available after' in result["detail"]:
				raise TooEarlyCancellationException(result)
			elif 'Error during' in result["detail"]:
				raise OrderProcessingException(result)
			elif 'Unsupported order type' in result["detail"]:
				raise UnsupportedOrderTypeException(result)
			elif result["detail"] == 'Technical works, please try again later':
				raise TechnicalWorksException(result)
			elif result["detail"] == 'Not available with this rent_time':
				raise RentTimeNotAvailableException(result)
			elif result["detail"] == 'Minimum 2 services, maximum 5 services':
				raise InvalidServiceCountException(result)
			else:
				raise OtherApiException(result)
		else:
			return result
