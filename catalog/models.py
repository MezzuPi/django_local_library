from django.db import models
from django.urls import reverse #generate URLs by reversing URL patterns
import uuid # Requerida para las instancias de libros unicos
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Genre(models.Model):
    """
    Modelo que representa un género literario (p. ej. ciencia ficción, poesía, etc.).
    """
    name = models.CharField(max_length=200, help_text="Ingrese el nombre del género (p. ej. Ciencia Ficción, Poesía Francesa etc.)")

    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo (p. ej. en el sitio de Administración)
        """
        return self.name
    
class Language(models.Model):
    """
    Modelo que representa el lenguage de un libro en particular
    """

    name = models.CharField(max_length=20, help_text='Introduce el idioma del libro', unique=True,)

    def get_absolute_url(self):
        return reverse('language-detail', args=[str(self.id)])

    def __str__(self):
        return self.name
 
    
class Book(models.Model):
    """
    Modelo que representa un libro(pero no uno especifico)
    """

    title = models.CharField(max_length=200)

    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)
    # ForeignKey porque un libro tiene solo un autor, pero un autor puede haber escrito varios libros
    # "Author" es un string, en lugar de objeto, porque la clase Author aun no ha sido declarada

    summary = models.TextField(max_length=1000, help_text="Ingrese una breve descripción del libro")

    isbn = models.CharField("ISBN", max_length=13, help_text='13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genre = models.ManyToManyField(Genre, help_text='Seleccione un genero para este libro')
    # ManyToManyField, porque un genero puede contener muchos libros, y un libro pertenecer a varios generos.
    # La clase Genre ya ha sido definida, entonces podemos especificar el objeto arriba.

    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def display_genre(self):
        """
        Crea una string para el genero, lo utilizamos para mostrarlo en Admin
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]]) 
    display_genre.short_description = 'Genre'

    def __str__(self):
        """
        String que representa al objeto Book
        """
        return self.title
    
    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular del Book
        """
        return reverse('book-detail', args=[str(self.id)])
    

class BookInstance(models.Model):
    """
    Modelo que representa una copia especifica de un libro (Que puede ser prestado por la biblioteca)
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='ID unico para este libro en particular en toda la biblioteca')
    
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)

    imprint = models.CharField(max_length=200)

    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Disponibilidad del libro')

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
    
    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        return f'{self.id} ({self.book.title})'
    

class Author(models.Model):
    """
    Modelo que representa un autor
    """

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    def get_absolute_url(self):
        """
        Retorna la url para acceder a una instancia particular de un autor.
        """
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
       
    class Meta:
        ordering = ['last_name']