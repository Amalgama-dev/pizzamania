from django.contrib import admin
from django.forms import ModelChoiceField
from main import models


class PizzaAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(models.Category.objects.filter(slug='pizza'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SushiAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(models.Category.objects.filter(slug='sushi'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(models.Category)
admin.site.register(models.Sushi, SushiAdmin)
admin.site.register(models.Pizza, PizzaAdmin)
admin.site.register(models.CartProduct)
admin.site.register(models.Cart)
admin.site.register(models.Customer)
admin.site.register(models.Order)