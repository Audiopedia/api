
import graphene

import audios.schema

class Query(audios.schema.Query, graphene.ObjectType):
    pass

class Mutation(audios.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)