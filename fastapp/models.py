from djongo import models


from bson import ObjectId
from .manager import *


class Users(AbstractUser):
    username = None
    name = models.TextField()
    email = models.EmailField(unique=True)
    countrycode = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    login_type = models.TextField()
    password = models.TextField()
    is_active = models.BooleanField(default=False)
    socialLoginId = models.TextField(blank=True, null=True)
    profileImage = models.TextField(blank=True, null=True)
    accessToken = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class VerifyEmail(models.Model):
    user_id = models.ForeignKey("Users", on_delete=models.CASCADE)
    otp = models.CharField(max_length=255)
    expire_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.FloatField()
    features = models.CharField(max_length=255)
    valid_days = models.IntegerField()
    trailing_allow = models.BooleanField(choices=[(True, "True"), (False, "False")])
    status = models.IntegerField(default=1)  # 1=Active, 0=Inactive
    payment_url = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.CharField(max_length=255)  # "admin"
    updated_by = models.CharField(max_length=255)  # "admin"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Questionnaire(models.Model):
    _id = models.ObjectIdField(
        primary_key=True, default=ObjectId, editable=False, auto_created=True
    )
    question = models.CharField(max_length=255)  # what your's gender?
    options = models.JSONField(blank=True, null=True)  # male,female,
    quetype = models.CharField(
        max_length=255,
        choices=[
            ("MCQ", "mutiple choices"),
            ("sliding", "sliding"),
            ("custom", "custom"),
        ],
    )  # "mutiple choices or sliding or custom"
    range = models.JSONField(
        blank=True, null=True
    )  # {"from":25, "to":30, "scale": "cm/in/kg/lbs"}
    inputtype = models.CharField(
        max_length=255
    )  # int, float, string, weight scale, hieght scale if qusetion type sliding or custom
    status = models.IntegerField(default=1)  # 1= Active 0= Inactive
    created_by = models.CharField(max_length=255)  # admin
    updated_by = models.CharField(max_length=255)  # admin
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserSubscriptions(models.Model):
    user_id = models.ForeignKey("Users", on_delete=models.CASCADE)
    plan_id = models.ForeignKey("SubscriptionPlan", on_delete=models.CASCADE)
    status = models.IntegerField(default=1)  # 1=Active, 2=trailing, 0=Cancel
    start_at = models.DateTimeField(auto_now_add=True)  # Default to current datetime
    end_at = models.DateTimeField()
    expiry = models.DateField()
    trail_ends_at = models.DateField(null=True, blank=True)  # Make it optional
    amount_paid = models.IntegerField(default=0)
    Transaction_Id = models.CharField(max_length=255)  # Trans1234
    paid_through = models.CharField(max_length=255)  # Stripe
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Fastingcycle(models.Model):
    name = models.CharField(max_length=255, unique=True)
    fasting = models.IntegerField(
        null=True, blank=True
    )  # Use null=True and blank=True for optional fields
    nonfasting = models.IntegerField(
        null=True, blank=True
    )  # Use null=True and blank=True for optional fields
    status = models.IntegerField(default=1)  # 1=Active, 0=Inactive
    description = models.CharField(
        max_length=255, null=True, blank=True
    )  # Use null=True and blank=True for optional fields
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserdailyFasting(models.Model):
    user_id = models.ForeignKey("Users", on_delete=models.CASCADE)
    fastingcycle_id = models.ForeignKey("Fastingcycle", on_delete=models.CASCADE)
    status = models.IntegerField(default=1)  # 1=Active, 2=Inactive, 0=cancel
    logDate = models.DateField()
    fastingDuration = models.CharField(max_length=255)  # In hours
    starting_time = models.DateTimeField()
    notes = models.CharField(max_length=255, null=True, blank=True)  # User notes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Ingredient(models.Model):
    _id = models.ObjectIdField(
        primary_key=True, default=ObjectId, editable=False, auto_created=True
    )
    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=10, choices=[("veg", "Veg"), ("non-veg", "Non-Veg")]
    )
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)


class Recipes(models.Model):
    _id = models.ObjectIdField(
        primary_key=True, default=ObjectId, editable=False, auto_created=True
    )
    name = models.CharField(max_length=255, unique=True)
    Ingredients = models.JSONField()
    servings = models.IntegerField()
    prepTime = models.IntegerField()  # minutes
    cookTime = models.IntegerField()  # minutes
    instructions = models.JSONField()
    imageUrls = models.JSONField()
    Meta_tags = models.JSONField()
    likes = models.FloatField(default=0)
    nutrition = models.JSONField()
    status = models.IntegerField(default=1)
    dietaryPreferences = models.JSONField()
    cuisineType = models.JSONField(default=list)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.DjongoManager()


class MealCategory(models.Model):
    _id = models.ObjectIdField(
        primary_key=True, default=ObjectId, editable=False, auto_created=True
    )
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    status = models.IntegerField(default=1)  # 1=Active, 0=Inactive
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MasterDietplan(models.Model):
    _id = models.ObjectIdField(
        primary_key=True, default=ObjectId, editable=False, auto_created=True
    )
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    status = models.IntegerField(default=1)  # 1=active, 0=Inactive
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DietplanRecipes(models.Model):
    _id = models.ObjectIdField(
        primary_key=True, default=ObjectId, editable=False, auto_created=True
    )
    master_dietplan_id = models.ForeignKey(MasterDietplan, on_delete=models.CASCADE)
    mealcategory_id = models.ForeignKey(MealCategory, on_delete=models.CASCADE)
    recipe_id = models.ForeignKey("Recipes", on_delete=models.CASCADE)
    status = models.IntegerField(null=True, blank=True)
    created_by = models.CharField(max_length=255, null=True, blank=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserMealPlan(models.Model):
    user_id = models.ForeignKey("Users", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    dietplan_id = models.ForeignKey(DietplanRecipes, on_delete=models.CASCADE)
    status = models.IntegerField(default=1)  # 1=Active, 0=Inactive
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserMealItem(models.Model):
    user_id = models.ForeignKey("Users", on_delete=models.CASCADE)
    mealcategory_id = models.ForeignKey(MealCategory, on_delete=models.CASCADE)
    day = models.CharField(max_length=255)
    recipeid = models.ForeignKey("Recipes", on_delete=models.CASCADE)
    status = models.IntegerField(default=1)  # 1=Active, 0=Inactive
    quantity = models.IntegerField()
    created_by = models.CharField(max_length=255, null=True, blank=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserActivity(models.Model):
    user_id = models.ForeignKey("Users", on_delete=models.CASCADE)
    waterIntake = models.CharField(max_length=255)
    timeInterval = models.IntegerField()
    status = models.IntegerField(default=1)  # 1=Active, 0=Inactive
    created_by = models.CharField(max_length=255, null=True, blank=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
