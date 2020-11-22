import sys
from graphqlclient import GraphQLClient
from random import randint
import codecs, json

client = GraphQLClient("https://net.ton.dev/graphql")
mutation_template = '''
mutation {
  postRequests(requests:[{id:"%(request_id)s",body:"%(base64_boc)s",expireAt:2e12}])
}
'''

def send_boc(client, boc):
  data = {'request_id':str(randint(0,2**32)), 'base64_boc': codecs.decode(codecs.encode(boc,'base64'),'utf8').replace('\n','')}
  r = json.loads(client.execute(mutation_template%data))
  print(r)
  
with open(sys.argv[1], "rb+") as f:
  send_boc(client, f.read())

