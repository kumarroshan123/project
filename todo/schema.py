import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db, ToDoItem, User
from auth import login_required

class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node,)

class ToDoItemType(SQLAlchemyObjectType):
    class Meta:
        model = ToDoItem
        interfaces = (graphene.relay.Node,)

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_users = SQLAlchemyConnectionField(UserType)
    all_todos = SQLAlchemyConnectionField(ToDoItemType)

class CreateToDoItem(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        time = graphene.String(required=True)
        image_url = graphene.String(required=False)

    todo = graphene.Field(lambda: ToDoItemType)

    @login_required
    def mutate(self, info, title, description, time, image_url=None):
        user_id = info.context['user'].get('sub')
        user = User.query.filter_by(id=user_id).first()
        if not user.is_pro and image_url:
            raise Exception('User does not have Pro license.')
        todo = ToDoItem(title=title, description=description, time=time, image_url=image_url, user_id=user.id)
        db.session.add(todo)
        db.session.commit()
        return CreateToDoItem(todo=todo)

class Mutation(graphene.ObjectType):
    create_todo = CreateToDoItem.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
