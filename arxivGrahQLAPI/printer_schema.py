import json
from schema import my_schema
import sys
from graphql.utils import schema_printer

my_schema_str = schema_printer.print_schema(my_schema)
fp = open("schema.graphql", "w")
fp.write(my_schema_str)
fp.close()