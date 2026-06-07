from app.DB.schema.todo_schema import TodoSchema
from app.DB.schema.user_schema import CreateUserSchema

# this is for, so that alembic can read the schema when it runs the migration, otherwise it will not be able to find the schema and will throw an error
__all__ = ["TodoSchema", "CreateUserSchema"] 