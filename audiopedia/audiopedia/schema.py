
import graphene

import audios.schema

class Query(audios.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)