from django import forms
from django.core.exceptions import ValidationError
from .models import *


class DietplanRecipesForm(forms.ModelForm):
    master_dietplan_id = forms.ModelChoiceField(
        queryset=MasterDietplan.objects.all(),
        to_field_name="_id",  # Use "_id" field as the value for the option
    )
    mealcategory_id = forms.ModelChoiceField(
        queryset=MealCategory.objects.all(),
        to_field_name="_id",  # Use "_id" field as the value for the option
    )
    recipe_id = forms.ModelChoiceField(
        queryset=Recipes.objects.all(),
        to_field_name="_id",  # Use "_id" field as the value for the option
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize the way options are displayed
        self.fields[
            "master_dietplan_id"
        ].label_from_instance = lambda obj: f"{obj.name} ({obj._id})"
        self.fields[
            "mealcategory_id"
        ].label_from_instance = lambda obj: f"{obj.name} ({obj._id})"
        self.fields[
            "recipe_id"
        ].label_from_instance = lambda obj: f"{obj.name} ({obj._id})"

    class Meta:
        model = DietplanRecipes
        fields = "__all__"
