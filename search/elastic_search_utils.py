from elasticsearch import Elasticsearch
from django.conf import settings

es = Elasticsearch(settings.ES_HOST, http_auth=(settings.ES_USER, settings.ES_PASSWORD))

class Search():
	"""docstring for Search"""
	conn_counter = 0
	def __init__(self):
		Search.conn_counter += 1
		# print('SEARCH CLASS COUNTER:', Search.conn_counter)


	def make_body_01(self, query:str):
		body = {
			"query": {
				"bool": {
					"should": [
						{
							"multi_match": {
								"query": query,
								"type": "cross_fields",
								"fields": [
									"facultate",
									"universitate",
									"localitate"
								],
								"operator": "or",
								"boost": 1
							}
						},
						{
							"multi_match": {
								"query": query,
								"type": "most_fields",
								"fields": [
									"facultate",
									"universitate",
									"localitate"
								],
								"fuzziness": "AUTO"
							}
						},
						{
							"dis_max": {
								"queries": [
									{"wildcard" : { "facultate" : {"value" : "*" + query + "*", "boost": 10}}},
									{"wildcard" : { "universitate" : {"value" : "*" + query + "*", "boost": 2}}},
									{"wildcard" : { "localitate" : {"value" : "*" + query + "*", "boost": 1}}},
								],
								"tie_breaker": 0.7,
								"boost": 0.1
							}
						}
					]
				}
			}
		}
		return body

	def schools(self, query:str, limit=10):
		if query:
			results = []
			for hit in es.search(body = self.make_body_01(query), index='facultati')['hits']['hits'][:limit]:
				data = {
				'id_facultate': hit['_source']['id_facultate'],
				'facultate': hit['_source']['facultate'], 
				'universitate': hit['_source']['universitate'], 
				'localitate': hit['_source']['localitate']}
				results.append(data)
			return results
		else:
			return None

	# def school_by_id(self, school_id):
	# 	if school_id:
	# 		hit = es.get(index='scoli', id=school_id)
	# 		data = {'doc_id': hit['_id'], 
	# 		'facultate': hit['_source']['facultate'], 
	# 		'universitate': hit['_source']['universitate'], 
	# 		'localitate': hit['_source']['localitate']}
	# 		return data
	# 	else:
	# 		return None

	# def professors(self, query:str, limit=10):
	# 	if query:
	# 		results = []
	# 		for hit in es.search(body = self.make_body_01(query), index='profesori')['hits']['hits'][:limit]:
	# 			data = {'doc_id': hit['_id'], 
	# 			'nume': hit['_source']['nume'],
	# 			'disciplina': hit['_source']['disciplina'],
	# 			'departament': hit['_source']['departament'],
	# 			'scoala': hit['_source']['scoala'],
	# 			'universitate': hit['_source']['universitate'],
	# 			'localitate': hit['_source']['localitate']}
	# 			results.append(data)
	# 		return results
	# 	else:
	# 		return None

	# def professor_by_id(self, doc_id):
	# 	if doc_id:
	# 		hit = es.get(index='profesori', id=doc_id)
	# 		data = {'doc_id': hit['_id'], 
	# 		'nume': hit['_source']['nume'],
	# 		'disciplina': hit['_source']['disciplina'],
	# 		'departament': hit['_source']['departament'],
	# 		'scoala': hit['_source']['scoala'],
	# 		'universitate': hit['_source']['universitate'],
	# 		'localitate': hit['_source']['localitate']}
	# 		return data
	# 	else:
	# 		return None

	# def professors_by_school_id(self, school_id):
	# 	if school_id:
	# 		body = {  
	# 		    "size": 2500,
	# 		    "query": {
	# 		        "term": {
	# 		          "id_scoala": {
	# 		            "value": school_id
	# 		          }
	# 		        }
	# 		      }
	# 		    }
	# 		results = []
	# 		for hit in es.search(body = body, index='profesori')['hits']['hits']:
	# 			data = {'doc_id': hit['_id'], 
	# 			'nume': hit['_source']['nume'],
	# 			'disciplina': hit['_source']['disciplina'],
	# 			'departament': hit['_source']['departament'],
	# 			'scoala': hit['_source']['scoala'],
	# 			'universitate': hit['_source']['universitate'],
	# 			'localitate': hit['_source']['localitate']}
	# 			results.append(data)
	# 		return results
	# 	else:
	# 		return None



es_search = Search()


# TESTING METHODS
if __name__ == '__main__':

	# Bool Matching Test (multiple query scores combined)
	print('##### Bool Matching #####')
	for hit in es_search.schools("fa", limit=1):
		print(hit)

	# # ID Matching Test
	# print('\n##### ID Matching #####\n', es_search.professor_by_id(3))

	# # Get professors by school id
	# print(es_search.professors_by_school_id(school_id=2))

	# # Get school by school id
	# print(es_search.school_by_id(school_id=2))