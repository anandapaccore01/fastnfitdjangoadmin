from django.contrib import admin
from .models import *
from .forms import *
from django.shortcuts import redirect


class Myadmin(admin.ModelAdmin):
    change_form_template = "base.html"


class RecipesAdmin(admin.ModelAdmin):
    def add_view(self, request, form_url="", extra_context=None):
        return redirect("createRecipe")


class QuestionnaireAdmin(admin.ModelAdmin):
    def add_view(self, request, form_url="", extra_context=None):
        return redirect("createQuestionnaire")


admin.site.register(Questionnaire, QuestionnaireAdmin)

# Register your models here.
admin.site.register(Users)
admin.site.register(SubscriptionPlan)
admin.site.register(Fastingcycle)
admin.site.register(Ingredient)
admin.site.register(Recipes, RecipesAdmin)

admin.site.register(MealCategory)
admin.site.register(MasterDietplan)
admin.site.register(UserSubscriptions)
admin.site.register(UserMealPlan)
admin.site.register(UserMealItem)
admin.site.register(UserdailyFasting)
admin.site.register(UserActivity)


class DietrecipeAdmin(admin.ModelAdmin):
    def add_view(self, request, form_url="", extra_context=None):
        return redirect("createDietplanrecipes")


admin.site.register(DietplanRecipes, DietrecipeAdmin)
