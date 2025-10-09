from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field
import uuid # Required for unique book instances

class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)"
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular genre instance."""
        return reverse('genre-detail', args=[str(self.id)]) #"pela página, ele procura o livro", pelo elemento, encontra-se sua url

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique',
                violation_error_message = "Genre already exists (case insensitive match)"
            ),
        ]

class Language(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Book(models.Model):
    """Model representing a book."""
    title = models.CharField(max_length=200)
    summary = models.TextField(max_length=1000)
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn''">ISBN number</a>')
    author = models.ForeignKey("Author", on_delete=models.RESTRICT, null=True)
    genre = models.ManyToManyField(Genre, on_delete=models.RESTRICT)
    language = models.ManyToManyField(Language, on_delete=models.RESTRICT)

    def __str__(self):
        """String for representing the Model object."""
        return f'self.title, self.author'
    
    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

    class Meta:
        ordering = ['title']
        
class BookInstance(models.Model):
    LOAN_STATUS = (
        ('m','maintance'), 
        ('o', 'on loan'), 
        ('a', 'available'), 
        ('r', 'reservated'))
    uniqueID = models.UUIDField(max_length=13, unique=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    due_back = models.DateField(null=True, blank=True) #pode ser criado e pode não ser emprestado
    status = models.CharField(max_length=1, choices=LOAN_STATUS, default='m')
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.TextField(max_length=200)

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'
    
    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('book-instance', args=[str(self.id)])
    
class Author(models.Model):
    name = models.CharField(max_length=30, unique=True)
    date_of_birth = models.DateField(null=True)
    date_of_death = models.DateField(null=True)

    class Meta:
        ordering = ['name']
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique',
                violation_error_message = "Name author already exists (case insensitive match)"
            ),
        ]

    def __str__(self):
        """String for representing the Model object."""
        return self.name
    
    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('author-detail', args=[str(self.id)])
    
