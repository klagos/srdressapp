from books.models import publicacion, puntuacion
import csv

def deleteTables():  
    libro.objects.all().delete()
    puntuacion.objects.all().delete() 

def popBooks():
	lista = []
	with open('publications.csv') as csv_file:
	    csv_reader = csv.reader(csv_file, delimiter=';')
	    line_count = 0
	    for row in csv_reader:
	        if line_count != 0:
	        	if len(row) == 5:
	        		idUser = int(row[0])
	        		usuario = str(row[1])
	        		pub = publicacion(idPub=idPub, idUs=idUs)
	        		lista.append(pub)
	        line_count += 1
	pub.objects.bulk_create(lista)

def popRating():
	lista = []
	with open('ratings.csv') as csv_file:
	    csv_reader = csv.reader(csv_file, delimiter=';')
	    line_count = 0
	    for row in csv_reader:
	        if line_count != 0:
	        	if len(row) == 3:
	        		idUs = int(row[0])
	        		idPub = int(row[1])
	        		punt = int(row[2]) # ira de 1 a 11, a ver que pasa :o
	        		rating = puntuacion(idUs=idUs, idPub=idPub, punt=punt)
	        		lista.append(rating)
	        line_count += 1
	puntuacion.objects.bulk_create(lista)

def populateDatabase():
    deleteTables()
    popBooks()
    popRating()
    print("Finished database population")
    
if __name__ == '__main__':
    populateDatabase()

