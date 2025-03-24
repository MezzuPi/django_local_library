from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre, Language
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import datetime

# Create your views here.ç

#@login_required
#@permission_required('catalog.can_mark_returned')
#@permission_required('catalog.can_edit')
def index(request):
    """
    Funcion vista para la pagina de inicio de la web
    """

    #Genera contadores de algunos de los objetos principales
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Libros disponibles (Estatus 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count() #All implicito por defecto

    # Contador generos
    num_generos = Genre.objects.all().count()

    # Contador libros con palabra "y"
    num_libros_con_y = Book.objects.filter(title__contains=' y ').count()

    # Numero de visitas al index, como está contado en la variable de sesion
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(
        request,
        'index.html',
        context = {
            'num_books':num_books, 'num_instances':num_instances, 'num_instances_available':num_instances_available, 'num_authors':num_authors, 'num_generos':num_generos, 'num_libros_con_y':num_libros_con_y, 'num_visits':num_visits,
        }
    )

# Lista y Detalles Libros, La lista tiene un loginrequiredmixin
class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = 5
    # context_object_name = 'my_book_list' #propio nombre para la lista como variable de plantilla
    # queryset = Book.objects.filter(title__contains='war')[:5] #Query para obtener 5 libros que contengan war
    # template_name = 'books/my_arbitrary_template_name_list.html' #nombre y ubicacion variables

class BookDetailView(generic.DetailView):
    model = Book

# Lista y Detalles Autores
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

# Vista para libros alquilados por un usuario loggedin
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Vista generica basada en clases que enumera los libros prestados al usuario actual
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
    
# Vista para ver todos los libros alquilados por los librarians
class LoanedBooksLibrarianView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_librarian.html'
    paginate_by = 10
    permission_required = ('catalog.can_mark_returned')

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
    
# Vista para que los librarians puedan cambiar las fechas de libros
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk = pk)

    #Si la request es post, procesamos los datos del formulario
    if request.method == 'POST':

        # Creamos una nueva instancia del formulario y lo llenamos con datos de la request (binding)
        form = RenewBookForm(request.POST)

        # Verificamos que el formulario es valido
        if form.is_valid():
            # Procesamos los datos en form.cleaned_data como necesitemos
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # Redirigimos a una nueva URL
            return HttpResponseRedirect(reverse('loanedbooks'))
        
        # Si el formulario no es valido:
        else:
            return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})

        
    # Si es una request GET creamos el formulario por defecto
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date':proposed_renewal_date,})

        return render(request, 'catalog/book_renew_librarian.html', context = {'form':form, 'bookinst':book_inst})
    
# Modificar Autores
class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death':'05/01/2018',}
    permission_required = ('catalog.can_mark_returned')

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = ('catalog.can_mark_returned')

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = ('catalog.can_mark_returned')

# Modificar Books
class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    # initial = 
    permission_required = ('catalog.can_mark_returned')

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    permission_required = ('catalog.can_mark_returned')

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = ('catalog.can_mark_returned')