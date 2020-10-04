
import graphene

import audios.schema import Query as audios_query

class Query(audios_query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)