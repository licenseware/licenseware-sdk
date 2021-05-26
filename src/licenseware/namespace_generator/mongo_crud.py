import uuid
import datetime
import logging
import licenseware.mongodata as m
from flask_restx import abort

#TODO
# ONE TO ONE
# ONE TO MANY
# MANY TO MANY
# All Child objects should be deleted when their owning Parent is deleted.



class MongoCrud:
	"""
		This class provides get, post, put, delete http methods.

		Needs a TenantId in the request header.	
		Decorator authorization_check makes sure that TenantId and auth_token are provided

		Query params are taken from request.args, '_id' parameter is just for swagger documentation.

	"""

	request_obj = None #This will be updated when a http request is made (see MongoRequest)

	#Fetch togglers for special cases
	distinct_key = None
	foreign_key  = None


	@property
	def params(self):
		params = {}
		if self.request_obj.args is None: return params
		params = dict(self.request_obj.args) or {}
		params.pop('tenant_id', None)
		return params

	@property
	def payload(self):
		payload = {}
		if self.request_obj.json is None: return payload
		if isinstance(self.request_obj.json, dict):
			payload = self.request_obj.json
			payload.pop('tenant_id', None)

		return payload
		
	@property
	def query(self):
		tenant = {'tenant_id': self.request_obj.headers.get("TenantId")}
		query  = { **tenant, **self.params,  **self.payload }
		# logging.warning(f"----- CRUD Request: {query}")
		return query


	def fetch_data(self, request_obj):
		self.request_obj = request_obj

		query = self.query

		# Special queries
		if 'foreign_key' in query:
			self.foreign_key = query.pop('foreign_key')
	
		if 'distinct_key' in query and self.foreign_key:
			self.distinct_key = query.pop('distinct_key')
			query.update({self.distinct_key: {"$exists": True}})


		results = m.fetch(match=query, collection=self.collection)

		if self.foreign_key and len(results) == 1:					
			foreign_keys = results[0][self.foreign_key]
			if isinstance(foreign_keys, str): 
				foreign_keys = [foreign_keys]
			
			query = {
				"tenant_id": self.query['tenant_id'],
				"_id": {"$in": foreign_keys}	
			}

			results = m.fetch(match=query, collection=self.collection)

			if self.distinct_key:
				results = sorted(list(set([v[self.distinct_key] for v in results])))

			# Toggle values back to None
			self.distinct_key = None
			self.foreign_key  = None


		if isinstance(results, str): abort(500, reason=results)
		if not results: abort(404, reason='Requested data not found')

		return results


	def update_data(self, request_obj):
		self.request_obj = request_obj
		
		updated_docs = m.update(
			schema=self.schema, 
			match=self.query,
			new_data=dict(self.query, **{"updated_at": datetime.datetime.utcnow().isoformat()}), 
			collection=self.collection,
			append=False
		)

		if updated_docs == 0:
			abort(404, reason='Query had no match')

		if isinstance(updated_docs, str):
			abort(500, reason=updated_docs)

		return "SUCCESS"


	def insert_data(self, request_obj):
		self.request_obj = request_obj

		data = dict(self.query, **{
			"_id": str(uuid.uuid4()), 
			"updated_at": datetime.datetime.utcnow().isoformat()}
		)
		
		inserted_docs = m.insert(
			schema=self.schema, 
			collection=self.collection,
			data=data
		)

		if len(inserted_docs) == 0:
			abort(404, reason='Could not insert data')

		if isinstance(inserted_docs, str):
			abort(500, reason=inserted_docs)

		return "SUCCESS"


	def delete_data(self, request_obj):
		self.request_obj = request_obj
		
		deleted_docs = m.delete(match=self.query, collection=self.collection)
		
		if deleted_docs == 0:
			abort(404, reason='Query had no match')

		if isinstance(deleted_docs, str):
			abort(500, reason=deleted_docs)

		return "SUCCESS"
