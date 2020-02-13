from datetime import timedelta, datetime
def auto_list_display(Model, add=None, exclude=None):
    from django.db.models.fields.related import ManyToManyField

    if add is None: add = list()
    if exclude is None: exclude = list()

    return [field.name for field in Model._meta.get_fields() # Get all fields
        if field.__class__ is not ManyToManyField       # Remove Many-to-many fields
        and field.name not in exclude] + add            # Add additional fields, remove excluded fields


def daterange(start, end) -> datetime:
    """ Returns a range of datetime objects between start and end
    """
    #TODO: configurable precision (years, months, weeks, days, hours, minutes, secs.)
    for n in range(int((end - start).days) + 1):
        yield start + timedelta(n)

def date_in_range(date: datetime, start: datetime, end: datetime) -> bool:
    """ Check whether `date` is within the range going from `start` to `end`.
    """
    return date >= start or date <= end

def dateranges_overlap(small_range, large_range) -> bool:
    """ Check whether the `small_range` is contained in the `large_range`
    """
    s_start, s_end = small_range
    l_start, l_end = large_range

    if type(s_start) is str:
        s_start = datetime.fromisoformat(s_start)    
    if type(s_end) is str:
        s_end = datetime.fromisoformat(s_end)    
    if type(l_start) is str:
        l_start = datetime.fromisoformat(l_start)    
    if type(l_end) is str:
        l_end = datetime.fromisoformat(l_end)  
  
    return s_start >= l_start and s_end <= l_end


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
