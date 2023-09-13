from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from .models import *
from bson import ObjectId
import json


# Create your views here.
def createRecipe(request):
    if request.method == "POST":
        print(request.POST)
        data = request.POST
        ingredient_ids = []
        print(data.getlist("Ingredient[name]"), data.getlist("ingredient[category]"))
        for name, category in zip(
            data.getlist("Ingredient[name]"), data.getlist("ingredient[category]")
        ):
            try:
                existing_ingredient = Ingredient.objects.get(name=name)
                if existing_ingredient:
                    ingredient_ids.append(existing_ingredient._id)
            except Ingredient.DoesNotExist:
                # If the ingredient does not exist, create a new one and append its ObjectId
                ingredient = Ingredient.objects.create(name=name, category=category)
                ingredient_ids.append(ingredient._id)

        print("ingredient_ids:", ingredient_ids)
        Ingredient_list = []
        for id, quantity, quantity_type in zip(
            ingredient_ids,
            data.getlist("ingredient[quantity]"),
            data.getlist("ingredient[quantity_type]"),
        ):
            print(id, quantity, quantity_type)
            INgredient = {
                "IngredientId": id,
                "quantity": quantity,
                "quantity_type": quantity_type,
            }
            Ingredient_list.append(INgredient)

        print("Ingredient_list:", Ingredient_list)
        try:
            existing_recipe = Recipes.objects.get(name=data.get("name"))
            if existing_recipe:
                messages.error(request, "this recipe is already exist")
                return render(request, "Recipe.html")
        except Recipes.DoesNotExist:
            recipe = Recipes.objects.create(
                name=data.get("name"),
                Ingredients=Ingredient_list,
                servings=data.get("serving"),
                prepTime=data.get("PrepTime"),
                cookTime=data.get("cookTime"),
                instructions=json.loads(data.get("instructions")),
                imageUrls=json.loads(data.get("Image")),
                Meta_tags=json.loads(data.get("tags")),
                likes=data.get("likes"),
                nutrition={
                    "carbs": data.get("carbs") + data.get("carbs_units"),
                    "calories": data.get("calories"),
                    "Protein": data.get("protein") + data.get("protein_units"),
                    "fats": data.get("fats") + data.get("fats_units"),
                },
                dietaryPreferences=json.loads(data.get("dietaryPreferences")),
                cuisineType=json.loads(data.get("cuisineType")),
                created_by=data.get("created_by"),
                updated_by=data.get("updated_by"),
            )
            recipe.save()

        return render(request, "Recipe.html")
    else:
        return render(request, "Recipe.html")


def createQuestionnaire(request):
    if request.method == "POST":
        data = request.POST
        print(type(data.getlist("options")))
        range_list = []
        options = []
        if data.get("quetype") == "MCQ":
            for option in data.getlist("options"):
                option1 = {"_id": str(ObjectId()), "text": option}
                options.append(option1)
        else:
            for From, To, scale in zip(
                data.getlist("rangefrom"),
                data.getlist("rangeto"),
                data.getlist("scale"),
            ):
                range = {"from": From, "to": To, "scale": scale}
                range_list.append(range)
        print(options)
        try:
            existing_question = Questionnaire.objects.get(question=data.get("question"))
            if existing_question:
                messages.error(request, "question is already exist")
                return render(request, "question.html")
        except Questionnaire.DoesNotExist:
            questions = Questionnaire.objects.create(
                question=data.get("question"),
                options=options,
                quetype=data.get("quetype"),
                range=range_list,
                inputtype=data.get("inputtype"),
                status=data.get("status"),
                created_by=data.get("created_by"),
                updated_by=data.get("updated_by"),
            )
            questions.save()
            messages.success(request, "Question added successfully")
            return render(request, "question.html")

    else:
        return render(request, "question.html")


def createDietplanrecipes(request):
    if request.method == "POST":
        data = {
            "master_dietplan_id": ObjectId(request.POST["master_dietplan_id"]),
            "mealcategory_id": ObjectId(request.POST["mealcategory_id"]),
            "recipe_id": ObjectId(request.POST["recipe_id"]),
        }
        print(data)
        form = DietplanRecipesForm(data)
        if form.is_valid():
            print(form.cleaned_data)
            dietplanrecipe = DietplanRecipes(
                master_dietplan_id=form.cleaned_data["master_dietplan_id"],
                mealcategory_id=form.cleaned_data["mealcategory_id"],
                recipe_id=form.cleaned_data["recipe_id"],
                status=request.POST["status"],
                created_by=request.POST["created_by"],
                updated_by=request.POST["updated_by"],
            )
            dietplanrecipe.save()
            messages.success(request, "Diet Plan Recipe added successfully")

            return render(request, "dietrecipe.html", {"form": form})
    else:
        form = DietplanRecipesForm()
        return render(request, "dietrecipe.html", {"form": form})
