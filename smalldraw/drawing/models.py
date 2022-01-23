import random
import math

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def words(self):
        return Word.objects.filter(category_id=self.pk)


class Word(models.Model):
    word = models.CharField(max_length=30, unique=True)
    category_id = models.ForeignKey(Category, on_delete=models.RESTRICT)

    def __str__(self):
        return self.word


class Game(models.Model):
    n_rounds = models.IntegerField()
    round = models.IntegerField(default=1)
    turn = models.BooleanField(default=False)
    drawing_finished = models.BooleanField(default=False)
    secret_word = models.ForeignKey(Word, blank=True, null=True, on_delete=models.RESTRICT)
    first_points = models.IntegerField(default=0)
    second_points = models.IntegerField(default=0)
    current_category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)

    @staticmethod
    def generate_words(number, category_id):
        words = Word.objects.filter(category_id=category_id)
        if not words:
            return {'error': 'no words found'}
        word_count = words.count()
        indexes = random.sample(range(1, word_count), min(number, word_count))
        return [words.all()[index].word for index in indexes]

    def start(self):
        self.turn = 0

    @staticmethod
    def points_converter(base_points, time_elapsed):
        if time_elapsed < 0 or base_points < 0:
            return 0
        normal_time = 15
        normalized_time = time_elapsed / normal_time
        if normalized_time <= 1 / math.sqrt(2):
            coef = 2 - normalized_time ** 2
        else:
            coef = 2 / (2 * normalized_time ** 2 + 1) + 0.5
        return base_points * coef

    def add_points(self, player, points):
        if player == 'first':
            self.first_points += points
        else:
            self.second_points += points
        self.save()

    def end_turn(self):
        if not self.drawing_finished:
            self.drawing_finished = True
            self.save()
            return True
        self.drawing_finished = False
        self.save()
        if self.turn:
            self.turn = False
            self.save()
            if self.round == self.n_rounds:
                return False
            self.round += 1
            return True
        self.turn = True
        self.save()
        return True

    def is_finished(self):
        return self.round >= self.n_rounds
