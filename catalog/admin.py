from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language
# Register your models here.

# admin.site.register(Book)
# inline BookInstance para BookAdmin
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0
# Nueva clase BookAdmin
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

# admin.site.register(Author)


# inline Books para Author
class BooksInline(admin.TabularInline):
    model = Book
    extra = 0
# Nueva clase AuthorAdmin
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline]
# Registrar la clase admin con el modelo asociado
admin.site.register(Author, AuthorAdmin)

admin.site.register(Genre)

# admin.site.register(BookInstance)
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        ('Data', {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availabilty', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

admin.site.register(Language)