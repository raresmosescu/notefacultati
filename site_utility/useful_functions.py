from django.core import serializers
import json

# Doesn't work with joins
def query_to_json_obj(query_set, first=0, last=-1):
	d = json.loads(serializers.serialize('json', query_set)[:])
	return d