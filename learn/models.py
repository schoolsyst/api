from django.db.models import *
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

zero_to_one_validator = [MinValueValidator(0, "This can't be a negative value"), 
                         MaxValueValidator(1, "This should be a value between 0 and 1")]

        
class Note(Model):
    subject        = ForeignKey(to='common.Subject',
                                related_name='notes',
                                on_delete=CASCADE)
    uuid           = UUIDField("UUID", 
                               default=uuid.uuid4, 
                               editable=False, 
                               unique=True)
                               
    name           = CharField(max_length=100)
    content        = TextField(blank=True, null=True)
    created        = DateTimeField()
    learnt         = FloatField(validators=zero_to_one_validator, default=0)
    last_modified  = DateTimeField(blank=True, null=True)
    

    def __str__(self):
        return self.name
    
    
class Test(Model):
    notes    = ManyToManyField(Note, related_name='tests')
    uuid     = UUIDField("UUID", 
                         default=uuid.uuid4, 
                         editable=False,
                         unique=True)

    due      = DateTimeField()
    created  = DateTimeField(auto_now_add=True)
    room     = CharField(max_length=100)
    details  = TextField(blank=True, null=True)
    
    def __str__(self):
        return ', '.join([ str(note) for note in self.notes.all() ])
    
    
    
    
class Grade(Model):
    test     = ForeignKey(to='learn.Test', 
                          related_name='grades',
                          on_delete=CASCADE)
    uuid     = UUIDField("UUID", 
                         default=uuid.uuid4, 
                         editable=False,
                         unique=True)

    added    = DateField(auto_now=True)
    actual   = FloatField(validators=zero_to_one_validator, blank=True, null=True)
    expected = FloatField(validators=zero_to_one_validator, blank=True, null=True)
    goal     = FloatField(validators=zero_to_one_validator, blank=True, null=True)
    weight   = FloatField(default=1)
    maximum  = FloatField()
    
    def __str__(self):
        return self.test.__str__()
    