# Nu am modificat functia de generare a succesorilor si functia de testare a scopului deoarece le-am folosit pe cele default ale algoritmului A*
# Euristicile le-am luat de pe site-ul http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html 
# Deoarece fisierele de output sunt deschise pentru "append", ele trebuie sa fie sterse inaintea unei noi rulari.
#In Terminal este afisat timpul de rulare (nr de pasi pe care il face functia a_star())

import math
#fisiere pt teste: 
# input_1.txt (drum de cost minim de lungime mai mare decat 5)
# input_2.txt (nu are solutii)
# input_3.txt (drum de cost minim de lungime 3-5)
# input_4.txt (o stare initiala care este si finala)




#euristici: 
#i,j reprezinta pozitia in patrice a noului "elev" introdus, iar iend,jend reprezinta pozitia in matrice a nodului scop (elevul care trebuie sa primeasca mesajul) 

def euristica1(i,j,iend,jend):  #Euclidean distance, squared
	dx=abs(i-iend)
	dy=abs(j-jend)
	rez=dx*dx+dy*dy
	D=1
	return D*rez

def euristica2(i,j,iend,jend):  #Manhattan distance
	dx=abs(i-iend)
	dy=abs(j-jend)
	rez=dx+dy
	D=2
	return D*rez

def euristica3(i,j,iend,jend): #Chebyshev distance (nu indeplineste conditia de admisibilitate.)
	dx = abs(i-iend)
	dy = abs(j-jend)
	D=1
	D2=math.sqrt(2)
	return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)	


class Nod:
	def __init__(self, info, h):
		self.info = info
		self.h = h

	def __str__ (self):
		return "({}, h={})".format(self.info, self.h)

	def __repr__ (self):
		return f"({self.info}, h={self.h})"


class Arc:
	def __init__(self, capat, varf, cost):
		self.capat = capat	
		self.varf = varf	
		self.cost = cost	



class Problema:   #la parametrii se afla si numarul fisierului de input si numarul euristicii
	def __init__(self,nr_input,nr_euristica):
		self.nrinput=nr_input
		self.nreuristica=nr_euristica
		self.noduri = []
		self.matrice=[]
		self.suparati=[]
                                             #salvez elevii din clasa intr-o matrice si pe cei suparati in alta matrice ca sa formez, ulterior, nodurile si arcele cu ajutor lor
		self.nod_scop=""
		if nr_input==1:
			fin=open("C:/Users/Mircea/Desktop/FeMeI/AN2/sem2/Inteligenta_artificiala/Partea2/proiect/pr1/lab6/input_1.txt","r+")
			self.fout=open("C:/Users/Mircea/Desktop/FeMeI/AN2/sem2/Inteligenta_artificiala/Partea2/proiect/pr1/lab6/output_1.txt","a")
		if nr_input==2:
			fin=open("C:/Users/Mircea/Desktop/FeMeI/AN2/sem2/Inteligenta_artificiala/Partea2/proiect/pr1/lab6/input_2.txt","r+")
			self.fout=open("C:/Users/Mircea/Desktop/FeMeI/AN2/sem2/Inteligenta_artificiala/Partea2/proiect/pr1/lab6/output_2.txt","a")
		if nr_input==3:
			fin=open("C:/Users/Mircea/Desktop/FeMeI/AN2/sem2/Inteligenta_artificiala/Partea2/proiect/pr1/lab6/input_3.txt","r+")
			self.fout=open("C:/Users/Mircea/Desktop/FeMeI/AN2/sem2/Inteligenta_artificiala/Partea2/proiect/pr1/lab6/output_3.txt","a")
		if nr_input==4:
			fin=open("C:/Users/Mircea/Desktop/FeMeI/AN2/sem2/Inteligenta_artificiala/Partea2/proiect/pr1/lab6/input_4.txt","r+")
			self.fout=open("C:/Users/Mircea/Desktop/FeMeI/AN2/sem2/Inteligenta_artificiala/Partea2/proiect/pr1/lab6/output_4.txt","a")
		
		vf = [line for line in fin]

		for i in range(len(vf)):
			flag1=0
			if(vf[i]!="suparati\n"):
				self.matrice.append(vf[i].split())
			else:
				
				for j in range(i+1,len(vf)):
					if(vf[j].split()[0]!="mesaj:"):
						self.suparati.append(vf[j].split())
					else:
						self.nod_scop=vf[j].split()[3]
						strsursa=vf[j].split()[1]
						flag1=1
						break
			if flag1==1:
				break
		

						
			
				

		n=len(self.matrice)
		m=len(self.matrice[0])
		iend=0
		jend=0

		for i in range(n):
			for j in range(m):
				if self.matrice[i][j]==self.nod_scop:
					iend=i
					jend=j
	


		#adaugare noduri
		for i in range(n):
			for j in range(m):
				if self.matrice[i][j]!=0:
					
					if nr_euristica==1:
						dist=euristica1(i,j,iend,jend)   
						self.noduri.append(Nod(self.matrice[i][j],dist))
						if self.matrice[i][j]==strsursa:
							self.nod_start=Nod(self.matrice[i][j],dist)
					if nr_euristica==2:
						dist=euristica2(i,j,iend,jend)   
						self.noduri.append(Nod(self.matrice[i][j],dist))
						if self.matrice[i][j]==strsursa:
							self.nod_start=Nod(self.matrice[i][j],dist)
					if nr_euristica==3:
						dist=euristica3(i,j,iend,jend)   
						self.noduri.append(Nod(self.matrice[i][j],dist))
						if self.matrice[i][j]==strsursa:
							self.nod_start=Nod(self.matrice[i][j],dist)

		self.arce = []
                #adaugare arce
		for i in range(n-2):
			j=0
			k=1
			while j<=m-2 and k<=m-1:
				#pentru j
				if [self.matrice[i][j],self.matrice[i][j+1]] not in self.suparati and self.matrice[i][j]!="liber" and self.matrice[i][j+1]!="liber" and [self.matrice[i][j+1],self.matrice[i][j]] not in self.suparati:
					self.arce.append(Arc(self.matrice[i][j],self.matrice[i][j+1],1))
				if i!=0:
					if [self.matrice[i][j],self.matrice[i-1][j]] not in self.suparati and self.matrice[i][j]!="liber" and self.matrice[i-1][j]!="liber" and [self.matrice[i-1][j],self.matrice[i][j]] not in self.suparati:
						self.arce.append(Arc(self.matrice[i][j],self.matrice[i-1][j],1))
				if [self.matrice[i][j],self.matrice[i+1][j]] not in self.suparati and self.matrice[i][j]!="liber" and self.matrice[i+1][j]!="liber" and [self.matrice[i+1][j],self.matrice[i][j]] not in self.suparati:
						self.arce.append(Arc(self.matrice[i][j],self.matrice[i+1][j],1))
				#pentru k
				if [self.matrice[i][k],self.matrice[i][k-1]] not in self.suparati and self.matrice[i][k]!="liber" and self.matrice[i][k-1]!="liber" and [self.matrice[i][k-1],self.matrice[i][k]] not in self.suparati:
					self.arce.append(Arc(self.matrice[i][k],self.matrice[i][k-1],1))
				if i!=0:
					if [self.matrice[i][k],self.matrice[i-1][k]] not in self.suparati and self.matrice[i][k]!="liber" and self.matrice[i-1][k]!="liber" and [self.matrice[i-1][k],self.matrice[i][k]] not in self.suparati:
						self.arce.append(Arc(self.matrice[i][k],self.matrice[i-1][k],1))
				if [self.matrice[i][k],self.matrice[i+1][k]] not in self.suparati and self.matrice[i][k]!="liber" and self.matrice[i+1][k]!="liber" and [self.matrice[i+1][k],self.matrice[i][k]] not in self.suparati:
						self.arce.append(Arc(self.matrice[i][k],self.matrice[i+1][k],1))
				j+=2
				k+=2

		for i in range(n-2,n):
			for j in range(m):
				if [self.matrice[i][j],self.matrice[i-1][j]] not in self.suparati and self.matrice[i][j]!="liber" and self.matrice[i-1][j]!="liber" and [self.matrice[i-1][j],self.matrice[i][j]] not in self.suparati:
						self.arce.append(Arc(self.matrice[i][j],self.matrice[i-1][j],1))
				if i!=n-1:
					if [self.matrice[i][j],self.matrice[i+1][j]] not in self.suparati and self.matrice[i][j]!="liber" and self.matrice[i+1][j]!="liber" and [self.matrice[i+1][j],self.matrice[i][j]] not in self.suparati:
						self.arce.append(Arc(self.matrice[i][j],self.matrice[i+1][j],1))
				if j!=0:
					if [self.matrice[i][j],self.matrice[i][j-1]] not in self.suparati and self.matrice[i][j]!="liber" and self.matrice[i][j-1]!="liber" and [self.matrice[i][j-1],self.matrice[i][j]] not in self.suparati:
						self.arce.append(Arc(self.matrice[i][j],self.matrice[i][j-1],1))
				if j!=m-1:
					if [self.matrice[i][j],self.matrice[i][j+1]] not in self.suparati and self.matrice[i][j]!="liber" and self.matrice[i][j+1]!="liber" and [self.matrice[i][j+1],self.matrice[i][j]] not in self.suparati:
						self.arce.append(Arc(self.matrice[i][j],self.matrice[i][j+1],1))
	






	def cauta_nod_nume(self, info):
		
		for nod in self.noduri:
			if nod.info == info:
				return nod
		return None




class NodParcurgere:

	problema=None	


	def __init__(self, nod_graf, parinte=None, g=0, f=None):
		self.nod_graf = nod_graf  	
		self.parinte = parinte  	
		self.g = g  	
		if f is None :
			self.f = self.g + self.nod_graf.h
		else:
			self.f = f


	def drum_arbore(self):
		
		nod_c = self
		drum = [nod_c]
		while nod_c.parinte is not None :
			drum = [nod_c.parinte] + drum
			nod_c = nod_c.parinte
		return drum


	def contine_in_drum(self, nod):
		
		
		nod_c = self
		while nod_c is not None :
			if nod.info == nod_c.nod_graf.info:
				return True
			nod_c = nod_c.parinte
		return False


	
	def expandeaza(self):
		
		
		l_succesori = []
		for arc in self.problema.arce:
			if self.nod_graf.info == arc.capat :
				l_succesori.append( (self.problema.cauta_nod_nume(arc.varf), arc.cost) )
		return l_succesori


	
	def test_scop(self):
		return self.nod_graf.info == self.problema.nod_scop


	def __str__ (self):
		parinte=self.parinte if self.parinte is None else self.parinte.nod_graf.info
		return f"({self.nod_graf}, parinte={parinte}, f={self.f}, g={self.g})"




#functie care afiseaza drumul de la ionel la dragos (in cazul asta) cautand in matrice parintele fierui nod pentru a putea stabili in ce sens s-a deplasat mesajul
def afish_copii(l,pr):
	sir=[]
	for x in l:
		if x.parinte==None and len(sir)==0:
			sir.append(str(x.nod_graf.info))
		if x.parinte!=None:
			for i in range(len( pr.matrice)):
				flag=0
				for j in range(len(pr.matrice[0])):
					if j<len(pr.matrice)-2:
						if sir[-1]==pr.matrice[i][j] and pr.matrice[i][j+1]==x.nod_graf.info and j%2==0:
							sir.append(" > ")
							sir.append(str(x.nod_graf.info))
							flag=1
							break
						
					if j<len(pr.matrice)-2:
						if sir[-1]==pr.matrice[i][j] and pr.matrice[i][j+1]==x.nod_graf.info and j%2==1:
							sir.append(" >> ")
							sir.append(str(x.nod_graf.info))
							flag=1
							break
						

					if sir[-1]==pr.matrice[i][j] and pr.matrice[i][j-1]==x.nod_graf.info and j%2==1:
						sir.append(" < ")
						sir.append(str(x.nod_graf.info))
						flag=1
						break
						

					if sir[-1]==pr.matrice[i][j] and pr.matrice[i][j-1]==x.nod_graf.info and j%2==0:
						sir.append(" << ")
						sir.append(str(x.nod_graf.info))
						flag=1
						break
						
					if i<len(pr.matrice)-1:
						if sir[-1]==pr.matrice[i][j] and pr.matrice[i+1][j]==x.nod_graf.info:
							sir.append(" v ")
							sir.append(str(x.nod_graf.info))
							flag=1
							break
						

					if sir[-1]==pr.matrice[i][j] and pr.matrice[i-1][j]==x.nod_graf.info:
						sir.append(" ^ ")
						sir.append(str(x.nod_graf.info))
						flag=1
						break
						
				if flag==1:
					break
					
					
		
	for i in range(len(sir)):
                pr.fout.write(sir[i])
	pr.fout.write("\n")
	pr.fout.write("\n")
		


def str_info_noduri(l):
	
	sir = "["
	for x in l:
		sir += str(x) + "  "
	sir += "]"
	return sir


def afis_succesori_cost(l):
	
	sir = ""
	for (x, cost) in l:
		sir += "\nnod: "+str(x)+", cost arc:"+ str(cost)
	return sir


def in_lista(l, nod):
	
	for i in range(len(l)):
		if l[i].nod_graf.info == nod.info:
			return l[i]
	return None


def a_star(pr,e,f):
   
    counter=0


    rad_arbore = NodParcurgere(NodParcurgere.problema.nod_start)
    open = [rad_arbore]  
    closed = []  
    gasit = False

    while len(open) > 0 :
        #print(str_info_noduri(open))	# afisam lista open
        #print(str_info_noduri(closed))
        #print("\n")
        counter+=1

        nod_curent = open.pop(0)	
        closed.append(nod_curent)	

        
        if nod_curent.test_scop():
            gasit = True
            break

        l_succesori = nod_curent.expandeaza()	
        for (nod_succesor, cost_succesor) in l_succesori:
            

            
            if (not nod_curent.contine_in_drum(nod_succesor)):

                
                g_succesor = nod_curent.g + cost_succesor
                f_succesor = g_succesor + nod_succesor.h 

                
                nod_parcg_vechi = in_lista(closed, nod_succesor)

                if nod_parcg_vechi is not None:	
                    if (f_succesor < nod_parcg_vechi.f):
                        closed.remove(nod_parcg_vechi)	
                        nod_parcg_vechi.parinte = nod_curent 
                        nod_parcg_vechi.g = g_succesor	
                        nod_parcg_vechi.f = f_succesor	
                        nod_nou = nod_parcg_vechi	

                else :
                    
                    nod_parcg_vechi = in_lista(open, nod_succesor)

                    if nod_parcg_vechi is not None:	
                        if (f_succesor < nod_parcg_vechi.f):
                            open.remove(nod_parcg_vechi)
                            nod_parcg_vechi.parinte = nod_curent
                            nod_parcg_vechi.g = g_succesor
                            nod_parcg_vechi.f = f_succesor
                            nod_nou = nod_parcg_vechi

                    else: 
                        nod_nou = NodParcurgere(nod_graf=nod_succesor, parinte=nod_curent, g=g_succesor)
                        

                if nod_nou:
                    
                    i=0
                    while i < len(open):
                        if open[i].f < nod_nou.f:
                            i += 1
                        else:
                            while i < len(open) and open[i].f == nod_nou.f and open[i].g > nod_nou.g:
                                i += 1
                            break

                    open.insert(i, nod_nou)


    #print("\n------------------ Concluzie -----------------------")
    if len(open) == 0 and not gasit:
        print("Lista open e vida, nu avem drum de la nodul start la nodul scop")
    else:
        if e==1 or e==2:
                print("Fisier:"+str(f)+" Euristica:"+str(e)+"\n"+"Timp: "+str(counter)+" pasi\n")
        pr.fout.write("Euristica "+str(e)+"\n")
        afish_copii(nod_curent.drum_arbore(),pr) 



#pentru fiecare fisier de input, testez algoritmul pe 3 euristici:

if __name__ == "__main__":
	#fisierul 1, euristica 1
	f=1
	e=1
	problema = Problema(f,e)
	NodParcurgere.problema = problema
	flag=0
	for i in range(len(problema.arce)):
		if problema.arce[i].capat==problema.nod_scop:
			flag=1

	if flag==0:
		problema.fout.write("Euristica "+str(e)+"\n")
		problema.fout.write("Nu se poate ajunge la "+str(problema.nod_scop)+"\n")
		problema.fout.write("\n")
	else:
		a_star(problema,e,f)
		

	#fisierul 1, euristica 2
	f=1
	e=2
	problema = Problema(f,e)
	NodParcurgere.problema = problema
	flag=0
	for i in range(len(problema.arce)):
		if problema.arce[i].capat==problema.nod_scop:
			flag=1

	if flag==0:
		problema.fout.write("Euristica "+str(e)+"\n")
		problema.fout.write("Nu se poate ajunge la "+str(problema.nod_scop)+"\n")
		problema.fout.write("\n")
	else:
		a_star(problema,e,f)
		

	#fisierul 1, euristica 3
	f=1
	e=3
	problema = Problema(f,e)
	NodParcurgere.problema = problema
	flag=0
	for i in range(len(problema.arce)):
		if problema.arce[i].capat==problema.nod_scop:
			flag=1

	if flag==0:
		problema.fout.write("Euristica "+str(e)+"\n")
		problema.fout.write("Nu se poate ajunge la "+str(problema.nod_scop)+"\n")
		problema.fout.write("\n")
	else:
		a_star(problema,e,f)
		

	#fisierul 2, euristica 1
	f=2
	e=1
	problema = Problema(f,e)
	NodParcurgere.problema = problema
	flag=0
	for i in range(len(problema.arce)):
		if problema.arce[i].capat==problema.nod_scop:
			flag=1

	if flag==0:
		problema.fout.write("Euristica "+str(e)+"\n")
		problema.fout.write("Nu se poate ajunge la "+str(problema.nod_scop)+"\n")
		problema.fout.write("\n")
	else:
		a_star(problema,e,f)
		

	#fisierul 2, euristica 2
	f=2
	e=2
	problema = Problema(f,e)
	NodParcurgere.problema = problema
	flag=0
	for i in range(len(problema.arce)):
		if problema.arce[i].capat==problema.nod_scop:
			flag=1

	if flag==0:
		problema.fout.write("Euristica "+str(e)+"\n")
		problema.fout.write("Nu se poate ajunge la "+str(problema.nod_scop)+"\n")
		problema.fout.write("\n")
	else:
		a_star(problema,e,f)
		

	#fisierul 2, euristica 3
	f=2
	e=3
	problema = Problema(f,e)
	NodParcurgere.problema = problema
	flag=0
	for i in range(len(problema.arce)):
		if problema.arce[i].capat==problema.nod_scop:
			flag=1

	if flag==0:
		problema.fout.write("Euristica "+str(e)+"\n")
		problema.fout.write("Nu se poate ajunge la "+str(problema.nod_scop)+"\n")
		problema.fout.write("\n")
	else:
		a_star(problema,e,f)
		

	#fisierul 3, euristica 1
	f=3
	e=1
	problema = Problema(f,e)
	NodParcurgere.problema = problema
	flag=0
	for i in range(len(problema.arce)):
		if problema.arce[i].capat==problema.nod_scop:
			flag=1

	if flag==0:
		problema.fout.write("Euristica "+str(e)+"\n")
		problema.fout.write("Nu se poate ajunge la "+str(problema.nod_scop)+"\n")
		problema.fout.write("\n")
	else:
		a_star(problema,e,f)
		

	#fisierul 3, euristica 2
	f=3
	e=2
	problema = Problema(f,e)
	NodParcurgere.problema = problema
	flag=0
	for i in range(len(problema.arce)):
		if problema.arce[i].capat==problema.nod_scop:
			flag=1

	if flag==0:
		problema.fout.write("Euristica "+str(e)+"\n")
		problema.fout.write("Nu se poate ajunge la "+str(problema.nod_scop)+"\n")
		problema.fout.write("\n")
	else:
		a_star(problema,e,f)
		

	#fisierul 3, euristica 3
	f=3
	e=3
	problema = Problema(f,e)
	NodParcurgere.problema = problema
	flag=0
	for i in range(len(problema.arce)):
		if problema.arce[i].capat==problema.nod_scop:
			flag=1

	if flag==0:
		problema.fout.write("Euristica "+str(e)+"\n")
		problema.fout.write("Nu se poate ajunge la "+str(problema.nod_scop)+"\n")
		problema.fout.write("\n")
	else:
		a_star(problema,e,f)
		

	#fisierul 4, euristica 1
	f=4
	e=1
	problema = Problema(f,e)
	NodParcurgere.problema = problema
	flag=0
	for i in range(len(problema.arce)):
		if problema.arce[i].capat==problema.nod_scop:
			flag=1

	if flag==0:
		problema.fout.write("Euristica "+str(e)+"\n")
		problema.fout.write("Nu se poate ajunge la "+str(problema.nod_scop)+"\n")
		problema.fout.write("\n")
	else:
		a_star(problema,e,f)
		

	#fisierul 4, euristica 2
	f=4
	e=2
	problema = Problema(f,e)
	NodParcurgere.problema = problema
	flag=0
	for i in range(len(problema.arce)):
		if problema.arce[i].capat==problema.nod_scop:
			flag=1

	if flag==0:
		problema.fout.write("Euristica "+str(e)+"\n")
		problema.fout.write("Nu se poate ajunge la "+str(problema.nod_scop)+"\n")
		problema.fout.write("\n")
	else:
		a_star(problema,e,f)
		

	#fisierul 4, euristica 3
	f=4
	e=3
	problema = Problema(f,e)
	NodParcurgere.problema = problema
	flag=0
	for i in range(len(problema.arce)):
		if problema.arce[i].capat==problema.nod_scop:
			flag=1

	if flag==0:
		problema.fout.write("Euristica "+str(e)+"\n")
		problema.fout.write("Nu se poate ajunge la "+str(problema.nod_scop)+"\n")
		problema.fout.write("\n")
	else:
		a_star(problema,e,f)
	
	problema.fout.close()
