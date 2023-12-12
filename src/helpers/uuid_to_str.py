from uuid import UUID


def uuid_to_str(obj):
    if isinstance(obj, UUID):
        return str(obj)
    raise TypeError(f"Tipo não serializável: {type(obj)}")