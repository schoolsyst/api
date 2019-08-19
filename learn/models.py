from django.db.models import *
from django.core.validators import MinValueValidator, MaxValueValidator

zero_to_one_validator = [MinValueValidator(0, "This can't be a negative value"), 
                         MaxValueValidator(1, "This should be a value between 0 and 1")]

        
class Note(Model):
    subject  = ForeignKey(to='common.Subject',
                          related_name='notes',
                          on_delete=CASCADE)
    name     = CharField(max_length=100)
    content  = TextField(blank=True, null=True)
    created  = DateTimeField(auto_now_add=True)
    filepath = CharField(max_length=1000)
    last_modified = DateTimeField()
    learnt   = FloatField(validators=zero_to_one_validator, default=0)
    

    def __str__(self):
        return self.name
    
    
class Test(Model):
    notes    = ManyToManyField(Note, related_name='tests')
    due      = DateTimeField()
    created  = DateTimeField(auto_now_add=True)
    room     = CharField(max_length=10)
    notes    = TextField()
    
    def __str__(self):
        return ', '.join([ str(notion) for notion in self.notions.all() ])
    
    
    
    
class Grade(Model):
    test     = ForeignKey(to='learn.Test', 
                          related_name='grades',
                          on_delete=CASCADE)
    added    = DateField(auto_now=True)
    actual   = FloatField(validators=zero_to_one_validator, blank=True, null=True)
    expected = FloatField(validators=zero_to_one_validator, blank=True, null=True)
    goal     = FloatField(validators=zero_to_one_validator, blank=True, null=True)
    weight   = FloatField(default=1)
    maximum  = FloatField()
    
    def __str__(self):
        return self.test.__str__()
    