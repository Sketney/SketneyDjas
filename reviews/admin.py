from django.contrib import admin

from reviews.models import Comment, Genre, Review, Title, User


class UserAdmin(admin.ModelAdmin):

    list_display = ('username', )


class TitleAdmin(admin.ModelAdmin):

    list_display = ('name', 'year', 'category')


class GenreAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'slug')


class ReviewAdmin(admin.ModelAdmin):

    def get_changeform_initial_data(self, request):
        get_data = super(
            ReviewAdmin, self).get_changeform_initial_data(request)
        get_data['created_by'] = request.user.pk
        return get_data


admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Comment)
