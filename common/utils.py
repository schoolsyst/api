def auto_list_display(Model, add=None, exclude=None):
    from django.db.models.fields.related import ManyToManyField

    if add is None: add = list()
    if exclude is None: exclude = list()
        
    return [field.name for field in Model._meta.get_fields() # Get all fields
        if field.__class__ is not ManyToManyField       # Remove Many-to-many fields
        and field.name not in exclude] + add            # Add additional fields, remove excluded fields


# @ https://www.w3resource.com/python-exercises/date-time-exercise/python-date-time-exercise-50.php
def daterange(date1, date2):
    """ Produces a range of datetime objects between date1 & date2
    """
    from datetime import timedelta
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)