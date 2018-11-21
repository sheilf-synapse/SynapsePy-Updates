
from .http_client import HttpClient

from .users import Users
from .nodes import Nodes
from .transactions import Transactions
from .subscriptions import Subscriptions

from .user import User
from .node import Node
from .transaction import Trans
from .subscription import Subscription

import requests
import api.models.errors as api_errors

import sys
import json
import logging

class Client():
	""" Client Record """

	# paths used for send requests to API
	paths = {
		'oauth': '/oauth/',
		'client': '/client',
		'users': '/users',
		'trans': '/trans',
		'nodes': '/nodes',
		'subs': '/subscriptions',
		'inst': '/institutions'
		}

	def __init__(self, **params):
		"""
		Args:
			client_id (str): API client id
			client_secret (str): API client secret
			devmode (bool): switches between sandbox and production base_url
		"""

		self.client_id = params['client_id']
		self.client_secret = params['client_secret']
		
		self.http = HttpClient(
			client_id=params['client_id'],
			client_secret=params['client_secret'],
			fingerprint=params['fingerprint'],
			ip_address=params['ip_address'],
			base_url='https://uat-api.synapsefi.com/v3.1' if params['devmode'] else 'https://api.synapsefi.com/v3.1',
			logging=params.get('logging', False)
			)

		self.logger = self.get_log(params.get('logging', False))

	def get_log(self, enable):
		'''Enables/Disables logs
		Args:
			enable (bool): enables if True, disables if False
		Returns:
			logger (Logger): logging.Logger object used to debug
		'''
		logging.basicConfig()
		logger = logging.getLogger("__name__")
		logger.setLevel(logging.DEBUG)
		logger.disabled = not enable

		return logger

	def create_user(self, payload, **params):
		"""
		Args:
			payload (json): user record
			json (json): JSON
		Returns:
			user (User): object containing User record
		"""
		self.logger.debug("Creating a new user")

		path = self.paths['users']
		response = self.http.post(path, payload)
		
		return User(response, self.http, full_dehydrate=True)
	
	def create_subcription(self, webhook_url, scope):
		'''
		Args:
			webhook_url (str): subscription url
			scope (list of str): API call types to subscribe to
		Returns:
			
		'''
		self.logger.debug("Creating a new subscription")

		path = self.paths['subs']

		payload = {
			'scope': scope,
			'url': webhook_url
		}

		return self.http.post(path, payload)

	def get_user(self, user_id, full_dehydrate=False, **params):
		"""Returns user object
		Args:
			user_id (Str): identification for user
		Returns:
			user (User): object containing User record
		"""
		self.logger.debug("getting a user")

		path = self.paths['users'] + '/' + user_id
		
		response = self.http.get(path, full_dehydrate=full_dehydrate, **params)

		return User(response, self.http, full_dehydrate=full_dehydrate)

	def get_subcription(self, sub_id):
		'''
		Args:
			sub_id (Str): subscription id
		Returns:
			(Subscription Object)
		'''
		self.logger.debug("getting a subscription")

		path = self.get_base() + self.paths['subs'] + '/' + sub_id
		response = self.http.get(path)

		return Subscription(response)

	def get_all_users(self, **params):
		"""Returns all user objects in a list
		Returns:
			(list of Json): json containing User records
		"""
		self.logger.debug("getting all users")

		path = self.paths['users']
		response = self.http.get(path, **params)

		return Users(self.http, response)

	def get_all_trans(self, **params):
		'''gets all client transactions
		Returns:
			(list of Transactions): list of all transaction records for client
		'''
		self.logger.debug("getting all transactions")
		
		path = self.paths['trans']
		response = self.http.get(path, **params)

		return Transactions(response)

	def get_all_nodes(self, **params):
		'''gets all client nodes
		Returns:
			(list of Nodes): list of all node records for client
		'''
		self.logger.debug("getting all nodes")
		
		path = self.paths['nodes']
		response = self.http.get(path)

		return Nodes(response)

	def get_all_subs(self, **params):
		'''
		'''
		self.logger.debug("getting all subscriptions")
		
		path = self.paths['subs']
		response = self.http.get(path, **params)

		return Subscriptions(response)

	def get_all_inst(self, **params):
		'''
		'''
		self.logger.debug("getting all institutions")
		
		path = self.paths['inst']

		response = self.http.get(path, **params)

		return response

	def issue_public_key(self, issue, scope):
		'''
		'''
		self.logger.debug("issuing a public key")
		
		path = self.paths['client']

		return self.http.get(path, issue_public_key=issue, scope=scope)['public_key_obj']

	def update_subcription(self, sub_id, **params):
		'''
		Args:
			sub_id (str): subscription id
		Returns:
			(Subscription): object containing subscription record
		'''
		self.logger.debug("updating subscription")
		
		valid_params = ['is_active', 'url', 'scope']

		url = self.params['subs'] + '/' + sub_id
		payload = {}

		for param in params:
			if param in valid_params:
				payload[param] = params[param]

		response = self.http.patch(url, payload)

		return Subscription(response)


