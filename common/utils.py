def auto_list_display(Model, add=None, exclude=None):
    from django.db.models.fields.related import ManyToManyField

    if add is None: add = list()
    if exclude is None: exclude = list()

    return [field.name for field in Model._meta.get_fields() # Get all fields
        if field.__class__ is not ManyToManyField       # Remove Many-to-many fields
        and field.name not in exclude] + add            # Add additional fields, remove excluded fields


def daterange(start, end):
    """ Returns a range of datetime objects between start and end
    """
    #TODO: configurable precision (years, months, weeks, days, hours, minutes, secs.)
    from datetime import timedelta
    for n in range(int((end - start).days) + 1):
        yield start + timedelta(n)

def hyperlinked_field_method(prop, prop2='uuid', name=None):
    if name is None: name = prop+'s'
    def hyperlinked_field(self, obj):
        subobj = getattr(obj, prop)
        if subobj is None: return None
        return f"http://localhost:8000/api/{name}/{getattr(subobj, prop2)}"

    return hyperlinked_field


def all_h_tags(dict_val=None, upto=6):
    tags = ['h' + str(i) for i in range(upto-1)]
    return tags if dict_val is None else {t: dict_val for t in tags}
