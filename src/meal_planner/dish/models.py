from django.db import models


# from http://stackoverflow.com/questions/1117564/set-django-integerfield-by-choices-name/1490069#1490069
class ChoiceField(models.IntegerField):
    def __init__(self, choices, **kwargs):
        if not hasattr(choices[0], '__iter__'):
                choices = zip(range(len(choices)), choices)
    
        self.val2choice = dict(choices)
        self.choice2val = dict((v, k) for k, v in choices)
    
        kwargs['choices'] = choices
        super(models.IntegerField, self).__init__(**kwargs)
    
    def to_python(self, value):
        return self.val2choice[value]
    
    def get_db_prep_value(self, choice, connection=None, prepared=None): # added connection=None, prepared=None
        return self.choice2val[choice]


# Custom Models
class Dish(models.Model):  # e.g. Sweet Potato Hash
    name = models.CharField(max_length=255)
    servingSize = models.IntegerField()
    recipe = models.TextField()
    
    def __unicode__(self):
        return self.name
    
class QuantityType(models.Model):  # e.g. teaspoon
    type = ChoiceField(('Volume', 'Mass'))
    label = models.CharField(max_length=255)
    factorFromNormal = models.FloatField() # e.g. 1000 mL (Normal) to liter, e.g. 1000 g (Normal) to kilograms, e.g. 5000IU of Vitamin A

    def __unicode__(self):
        return self.label

class Label(models.Model): # Paleo, Atkins
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name

class SuperSubLabels(models.Model):
    sub = models.ForeignKey(Label, related_name='sub')  # e.g. Paleo
    super = models.ForeignKey(Label, related_name='super')  # e.g. Gluten-Free

    def __unicode__(self):
        return self.sub + " is " + self.super

class Ingredient(models.Model):  # e.g. extra virgin olive oil
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name

class DishIngredients(models.Model):
    dish = models.ForeignKey(Dish)  # e.g. Sweet Potato Hash
    ingredient = models.ForeignKey(Ingredient) # e.g. extra virgin olive oil
    quantity = models.FloatField() # e.g. 1.5 
    quantityType = models.ForeignKey(QuantityType) # e.g. tablespoons
    
    def __unicode__(self):
        return "%f %s of %s in %s" (self.quantity, ["g", "mL"][bool(self.quantityType == 'v')], self.ingredient, self.dish)

class IngredientLabel(models.Model):
    ingredient = models.ForeignKey(Ingredient) # almond flour
    label = models.ForeignKey(Label) # e.g. Paleo

    def __unicode__(self):
        return self.ingredient + " is " + self.label

class Nutrient(models.Model):
    name = models.CharField(max_length=255)
    dailyValuePercentPerUnit = models.FloatField()
    
    def __unicode__(self):
        return self.name

class IngredientNutrient(models.Model):
    ingredient = models.ForeignKey(Ingredient)
    nutrient = models.ForeignKey(Nutrient)
    ingredientAmount = models.FloatField()
    nutrientAmount = models.FloatField()
    
    def __unicode__(self):
        return "%f of %s has %f of %s" (self.ingredientAmount, self.ingredient, self.nutrientAmount, self.nutrient)

class Meal(models.Model):
    name = models.CharField(max_length=255) # breafast, lunch, dinner, snack, etc
    
    def __unicode__(self):
        return self.name

class DishMeal(models.Model):
    dish = models.ForeignKey(Dish)
    date = models.DateField()
    meal = models.ForeignKey(Meal)

    def __unicode__(self):
        return self.dish + " is for " + self.meal + " on " + self.date 



