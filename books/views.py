from django.shortcuts import render
from books.models import libro, puntuacion
from books.populate import populateDatabase
from books.recommendations import  transformPrefs, calculateSimilarItems, getRecommendations, getRecommendedItems, topMatches
from books.forms import UserForm, BookForm
import shelve

# Create your views here.

def loadDict():
	Prefs={}
	shelf = shelve.open("dataRS.dat")
	ratings = puntuacion.objects.all()
	for ra in ratings:
		user = int(ra.idUs)
		if user not in Prefs:
			Prefs[user] = {}
		itemid = int(ra.isbn)
		rating = int(ra.punt)
		Prefs[user][itemid] = rating
	shelf['Prefs']=Prefs
	shelf['ItemsPrefs']=transformPrefs(Prefs)
	shelf['SimItems']=calculateSimilarItems(Prefs, n=5)
	shelf.close()


def index(request): 
    return render(request,'index.html')

def populateDB(request):
    populateDatabase() 
    return render(request,'populate.html')

def loadRS(request):
    loadDict()
    return render(request,'loadRS.html')

# Apartado C

def userReview(request):
    if request.method=='GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            revs = puntuacion.objects.filter(idUs=idUser)
            num = []
            title = []
            stars = []
            for rev in revs:
            	book = rev.isbn
            	booktitle = libro.objects.filter(isbn=book)[0].titulo
            	star = rev.punt
            	num.append(book)
            	title.append(booktitle)
            	stars.append(star)
            items = zip(num,title,stars)
            return render(request,'userReview.html', {'user': idUser, 'items': items})
    form = UserForm()
    return render(request,'search_user.html', {'form': form})

# Apartado D

def bestBooks(request):
    books = []
    shelf = shelve.open("dataRS.dat")
    Prefs = shelf['ItemsPrefs']
    for lib in Prefs:
    	count = 0
    	for user in Prefs[lib]:
    		count+=Prefs[lib][user]
    	punt = float(count)/float(len(Prefs[lib]))
    	books.append((punt, lib))
    books.sort(reverse=True)
    books = books[:3]
    final = []
    for book in books:
    	obj = libro.objects.filter(isbn=book[1])[0]
    	title = obj.titulo
    	autor = obj.autor
    	final.append((book[1], title, autor, book[0]))
    return render(request,'bestBooks.html', {'books': final})

# Apartado E

def simBooks(request):
    if request.method=='GET':
        form = BookForm(request.GET, request.FILES)
        if form.is_valid():
            bookID = form.cleaned_data['id']
            shelf = shelve.open("dataRS.dat")
            ItemsPrefs = shelf['ItemsPrefs']
            shelf.close()
            if bookID in ItemsPrefs:
                recommended = topMatches(ItemsPrefs, int(bookID),n=5)
                lib = []
                similar = []
                for re in recommended:
                    lib.append(libro.objects.get(isbn=re[1]).isbn)
                    similar.append(re[0])
                    items = zip(lib, similar)
                return render(request,'simBook.html', {'book': bookID, 'items': items})
            else:
                return render(request, 'simBook.html')
    form = BookForm()
    return render(request,'search_book.html', {'form': form})

# Apartado F

def recommendedBooksUser(request):
    if request.method=='GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            shelf.close()
            if idUser in Prefs:
                rankings = getRecommendations(Prefs,int(idUser))
                recommended = rankings[:10]
                books = []
                scores = []
                for re in recommended:
                    books.append(libro.objects.get(isbn=re[1]))
                    scores.append(re[0])
                items= zip(books,scores)
                return render(request,'recommendationItems.html', {'user': idUser, 'items': items})
            else:
                return render(request,'recommendationItems.html')
    form = UserForm()
    return render(request,'search_user.html', {'form': form})
