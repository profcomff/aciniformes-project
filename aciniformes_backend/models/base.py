import re
from sqlalchemy.orm import declared_attr, as_declarative
from sqlalchemy.orm import registry

mapper_registry = registry()


@as_declarative()
class BaseModel:
    """Base class for all database entities"""

    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        """Generate database table name automatically.
        Convert CamelCase class name to snake_case db table name.
        """
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()
