from django.db.models import *
from django.core.validators import MinValueValidator, MaxValueValidator

zero_to_one_validator = [MinValueValidator(0, "The progress can't be a negative value"), 
                         MaxValueValidator(1, "The progress should be a value between 0 and 1")]

# Create your models here.
class Notion(Model):
    subject  = ForeignKey(to='common.Subject',
                          related_name='notions',
                          on_delete=CASCADE)
    
    name     = CharField(max_length=200)
    slug     = SlugField()
    progress = FloatField(validators=zero_to_one_validator, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    
class Note(Model):
    notion   = ForeignKey(to='learn.Notion',
                          related_name='notes',
                          on_delete=CASCADE)
    
    name     = CharField(max_length=100)
    content  = TextField()
    created  = DateTimeField(auto_now_add=True)
    filepath = FilePathField()
    lastModified = DateTimeField()
    
    def __str__(self):
        return self.name
    
    
class Test(Model):
    notions  = ManyToManyField(Notion, related_name='tests')
    
    due      = DateTimeField()
    created  = DateTimeField(auto_now_add=True)
    room     = CharField(max_length=10)
    notes    = TextField()
    
    def __str__(self):
        return ', '.join([ str(notion) for notion in self.notions ])
    
    
    
    
class Grade(Model):
    test     = ForeignKey(to='learn.Test', 
                          related_name='grades',
                          on_delete=CASCADE)
    
    actual   = FloatField(validators=zero_to_one_validator)
    expected = FloatField(validators=zero_to_one_validator)
    goal     = FloatField(validators=zero_to_one_validator)
    weight   = FloatField()
    maximum  = FloatField()
    
    def __str__(self):
        return self.test.__str__()
    