
def transfer_fk(from_, to):
    for rel in from_._meta.get_all_related_objects():
        objects = getattr(from_, rel.get_accessor_name()).all()
        for o in objects:
            print(repr(getattr(o, rel.field.name)), repr(from_))
            if getattr(o, rel.field.name) == from_:
                setattr(o, rel.field.name, to)
                o.save()
