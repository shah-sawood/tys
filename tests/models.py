"""Model Layer"""
from django.db import models

# Create your models here.
class Category(models.Model):
    """Category Model"""

    image = models.ImageField(
        upload_to="static/tests/category/images/",
        default="static/tests/category/images/default.png",
    )
    description = models.TextField(blank=True)
    name = models.CharField(max_length=72, unique=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Extra info about category model"""

        verbose_name_plural = "Categories"

    def get_id(self):
        """returns id for this category"""
        return self.id

    def get_image(self):
        """returns category image for this category"""
        return self.image

    def get_image_url(self):
        """returns category image url"""
        return self.get_image().url

    def get_description(self):
        """returns category_description"""
        return self.description

    def get_name(self):
        """returns cat_name"""
        return self.name

    def get_date_updated(self):
        """returns the date on which this category was updated"""
        return self.date_updated

    def get_date_created(self):
        """returns the date on which the category was created"""
        return self.date_created

    def get_questions(self):
        """returns all questions for this category"""
        return self.questions.filter(published=True)

    def get_num_of_questions(self):
        """returns number of questions in this category"""
        return self.get_questions().count()

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(*args, **kwargs)


class Question(models.Model):
    """Question Model"""

    choices = ((True, "Published"), (False, "Not published"))
    statement = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="questions"
    )
    published = models.BooleanField(default=False, choices=choices)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def get_id(self):
        """returns id for this question."""
        return self.id

    def get_statement(self):
        """returns statement of the question."""
        return self.statement

    def get_category(self):
        """returns category for this question."""
        return self.category

    def is_published(self):
        """returns True if the question is published otherwise False."""
        return self.published

    def get_date_updated(self):
        """returns the date on which this question was updated."""
        return self.date_updated

    def get_date_created(self):
        """returns the date on which this question was created."""
        return self.date_created

    def get_correct_option(self):
        """returns correct option for this question"""
        return self.options.get(correct=True)

    def get_options(self):
        """returns all options for this question."""
        return self.options.all()

    def __str__(self):
        return f"{self.statement}"


class Choice(models.Model):
    """choice model"""

    option = models.CharField(max_length=300)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="options"
    )
    correct = models.BooleanField(default=False)

    def get_id(self):
        """returns id for this option"""
        return self.id

    def get_question(self):
        """returns the question with which this option is associated"""
        return self.question

    def get_option_text(self):
        """returns the text of current choice"""
        return self.option

    def is_correct(self):
        """returns true if the option correct otherwise false"""
        return self.correct

    def __str__(self):
        return f"{self.option}"

    def save(self, *args, **kwargs):
        if self.get_question().get_options().count() > 4:
            raise ValueError("Choices must be less than or equal to 4.")
        super().save(*args, **kwargs)


class File(models.Model):
    file = models.FileField(upload_to="static/tests/files/questions/")
    category = models.ForeignKey(
        Category, related_name="files", on_delete=models.CASCADE
    )
