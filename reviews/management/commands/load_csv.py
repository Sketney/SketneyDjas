from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404
from get_reader import get_reader

from reviews.models import Category, Comment, Genre, Review, Title, User

file_path = 'static/data/'


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        reader = get_reader(file_path + 'genre.csv')
        next(reader, None)
        for row in reader:
            obj, created = Genre.objects.get_or_create(
                id=row[0],
                name=row[1],
                slug=row[2]
            )
        self.stdout.write(self.style.SUCCESS('Загрузка genre прошла успешно.'))

        reader = get_reader(file_path + 'category.csv')
        next(reader, None)
        for row in reader:
            obj, created = Category.objects.get_or_create(
                id=row[0],
                name=row[1],
                slug=row[2]
            )
        self.stdout.write(
            self.style.SUCCESS('Загрузка category прошла успешно.'))

        reader = get_reader(file_path + 'titles.csv')
        next(reader, None)
        for row in reader:
            obj, created = Title.objects.get_or_create(
                id=row[0],
                name=row[1],
                year=row[2],
                category=get_object_or_404(Category, id=row[3])
            )
        self.stdout.write(self.style.SUCCESS('Загрузка title прошла успешно.'))

        reader = get_reader(file_path + 'users.csv')
        next(reader, None)
        for row in reader:
            obj, created = User.objects.get_or_create(
                id=row[0],
                username=row[1],
                email=row[2],
                role=row[3],
                bio=row[4],
                first_name=row[5],
                last_name=row[6]
            )
        self.stdout.write(self.style.SUCCESS('Загрузка users прошла успешно.'))

        reader = get_reader(file_path + 'review.csv')
        next(reader, None)
        for row in reader:
            obj, created = Review.objects.get_or_create(
                id=row[0],
                title_id=get_object_or_404(Title, id=row[1]),
                text=row[2],
                author=get_object_or_404(User, id=row[3]),
                score=row[4],
                pub_date=row[5]
            )
        self.stdout.write(
            self.style.SUCCESS('Загрузка review прошла успешно.'))

        reader = get_reader(file_path + 'comments.csv')
        next(reader, None)
        for row in reader:
            obj, created = Comment.objects.get_or_create(
                id=row[0],
                review_id=get_object_or_404(Review, id=row[1]),
                text=row[2],
                pub_date=row[3]
            )
        self.stdout.write(
            self.style.SUCCESS('Загрузка comments прошла успешно.'))
