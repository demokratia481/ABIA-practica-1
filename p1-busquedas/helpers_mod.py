from inspect import getsource
from IPython.display import HTML
from IPython.display import display

from collections import Counter, defaultdict
from random import Random, randrange
import math


def psource(*functions):
    """Print the source code for the given function(s)."""
    source_code = '\n\n'.join(getsource(fn) for fn in functions)
    try:
        from pygments.formatters import HtmlFormatter
        from pygments.lexers import PythonLexer
        from pygments import highlight

        display(HTML(highlight(source_code, PythonLexer(), HtmlFormatter(full=False))))

    except ImportError:
        print(source_code)
        
class CountCalls:
    """Delegate all attribute gets to the object, and count them in ._counts"""
    def __init__(self, obj):
        self._object = obj
        self._counts = Counter()
        
    def __getattr__(self, attr):
        "Delegate to the original object, after incrementing a counter."
        self._counts[attr] += 1
        return getattr(self._object, attr)


def report(searchers, problems, verbose=True):
    """Show summary statistics for each searcher (and on each problem unless verbose is false)."""
    for searcher in searchers:
        print(searcher.__name__ + ':')
        total_counts = Counter()
        for p in problems:
            prob   = CountCalls(p)
            soln   = searcher(prob)
            counts = prob._counts; 
            counts.update(actions=len(soln), cost=soln.path_cost)
            total_counts += counts
            if verbose: report_counts(counts, str(p)[:40])
        report_counts(total_counts, 'TOTAL\n')
        
def report_counts(counts, name):
    """Print one line of the counts report."""
    #print('{:9,d} nodes |{:9,d} goal |{:5.0f} cost | {}'.format(
    #      counts['result'], counts['is_goal'], counts['cost'], name))
    print('{:9,d} nodes |{:5.0f} cost | {}'.format(
          counts['result'], counts['cost'], name))


def generate_random_board ():
    """ Generamos una instancia aleatoria de un tablero para el 8-Puzzle """
    goal=(0, 1, 2, 3, 4, 5, 6, 7, 8)
    goalList = list(goal)
    for i in range(100):
        irnd=randrange(4)
        blankIdx=goalList.index(0)        
        if irnd == 0: #UP
            newBlankIdx = blankIdx-3           
            if newBlankIdx > 0: 
                a=goalList[newBlankIdx]                
                b=goalList[blankIdx]                
                goalList[newBlankIdx] = b
                goalList[blankIdx] = a
        elif irnd == 1: #RIGHT
            if blankIdx not in (2,5,8):
                newBlankIdx = blankIdx+1                
                a=goalList[newBlankIdx]
                b=goalList[blankIdx]
                goalList[newBlankIdx] = b
                goalList[blankIdx] = a
        elif irnd == 2: #DOWN
            newBlankIdx = blankIdx+3            
            if newBlankIdx <= 8:                         
                a=goalList[newBlankIdx]
                b=goalList[blankIdx]
                goalList[newBlankIdx] = b
                goalList[blankIdx] = a
        elif irnd == 1: #LEFT
            if blankIdx not in (0,3,6):
                newBlankIdx = blankIdx-1                
                a=goalList[newBlankIdx]
                b=goalList[blankIdx]
                goalList[newBlankIdx] = b
                goalList[blankIdx] = a   
        #print (goalList)
    return tuple(goalList)

def generate_8puzzle_problems (n=10):
    """ Generamos n instancias aleatorias de problemas para el 8-Puzzle """
    problems = list()
    for i in range (n):
        problems.append(generate_random_board())
    return problems


class Localizaciones ():

    def __init__ (self, filename='./data/grafo8cidades.txt'):
        self.filename = filename
        file = open(filename, 'r')
        Lines = file.readlines()

        count = -1
        self.nciudades = 0 
        self.tablaciudades = dict()
        for line in Lines:
            if count == -1:
                self.nciudades = int(line.strip().split()[0])        
            else:
                tokens = line.strip().split()
                self.tablaciudades[count]=tuple((float(tokens[0]),float(tokens[1])))                

            count+=1
    
        self.matriz = []
        for c1 in range(self.nciudades):
            a = [0]*self.nciudades
            self.matriz.append(a)
            for c2 in range(self.nciudades):
                self.matriz[c1][c2] = self.__distancia_semiverseno__(c1, c2)
    
    def __distancia_semiverseno__ (self, c1, c2):
        radioTierra = 6371
        lat1 = math.radians(self.tablaciudades[c1][0]);
        lon1 = math.radians(self.tablaciudades[c1][1]);
        lat2 = math.radians(self.tablaciudades[c2][0]);
        lon2 = math.radians(self.tablaciudades[c2][1]);
        
        sinChi = math.sin((lat2 - lat1) / 2);
        sinLambda = math.sin((lon2 - lon1) / 2);

        raiz = (sinChi * sinChi) + math.cos(lat1) * math.cos(lat2) * (sinLambda * sinLambda);

        return 2 * radioTierra * math.asin(math.sqrt(raiz));
    
    def distancia (self, c1, c2):        
        return self.matriz [c1][c2]
    

