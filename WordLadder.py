import sys
import heapq
from tkinter import *

class Graph(object):
    '''
    Creating graph, making functions including patterns, unvisited and minpath.
    This graph uses the words as nodes, and finds the shortest path between these
    nodes/words to find the shortest path that involves the least amount of vowel
    changes as possible.

    '''
    def __init__(self, words, size):
        self.word_patterns = {}
        self.size = size

        for word in words:
            if len(word) != size: #getting words of the same lenght only
                continue
            for p in self.patterns(word):
                if p not in self.word_patterns:
                    self.word_patterns[p] = []
                #each variation of the word is added to the dictionary of word patterns
                self.word_patterns[p].append(word)

    def patterns(self, word):
        '''
        Replaces each letter of the inputted word with a question mark ? and returns
        a list containing all of the altered words.
        Arguments:
            word - the word for which each letter will be replaced
        Returns:
            a list of the variations of the inputted word
        '''
        p = []
        for i in range(len(word)):
            letters = list(word)#splitting up the letters to form a list
            letters[i] = '?'
            p.append((i,''.join(letters)))#combining letters to form a string again
        return p

    def unvisited(self, word, visited):
        '''
        Checks to see if the word that may be added to path has already been
        visited or is part of the path. This prevents the algorithm from becoming
        stuck in a loop.
        Arguments:
            word - a candidate for becoming part of the path
            visited - a dictionary of the visited nodes or words and their costs
        Returns:
            a list of words which can be candidates to add to the path
        '''
        words = []
        for p in self.patterns(word):
            #candidates are all the words that are variations of the initial word,
            #as listed in the word_patterns dictionary
            candidates = self.word_patterns.get(p)
            if candidates is None:
                continue
            for cand in candidates:
                if cand not in visited:
                    # adding candidates iff they have not been
                    #already explored/used/seen
                    words.append(cand)
        return words # list of unvisited words that could be added to path

    def min_path(self, start, end):
        '''
        Computes the minimum (shortest) path from start to end, while following
        the rules of the Word Ladder problem.

        Arguments:
            start - start word
            end - end word

        Returns:
            None
        '''
        visited = {} #dictionary of words that have been explored and their cost
        frontier = [] # the queue which the heap uses

        #pushing the tuple of the distance, current word, and path so far onto heap
        heapq.heappush(frontier, (0, start, [start]))

        while len(frontier) > 0:

            #getting word for the smallest distance
            distance, word, path = heapq.heappop(frontier)

            if word == end:
                return path #ends by returning the shortest word ladder/path

            for adjacent in self.unvisited(word, visited):
                zipped = zip(path[len(path)-1],path[len(path)-2])
                for i,j in zipped:
                    if i != j: #adding to distance if the letter change is by vowels
                        if i == 'a' or 'e' or 'i' or 'o' or 'u' or 'y':
                            distance += 1
                cost = distance + hamming(adjacent, end)
                visited[adjacent] = cost

                #adding new word to current path, pushing onto heap
                heapq.heappush(frontier, (cost, adjacent, path + [adjacent]))
        return None

def hamming(start, end):
    '''
    Calculates the Hamming distances between words.
    The Hamming distance between two strings of equal length is the number of
    positions at which the corresponding symbols are different.
    Hamming distance measures the minimum number of substitutions required to
    change one string into the other.

    Arguments:
        start - start word
        end - end word

    Returns:
        int - Hamming distance between start and end

    Examples:
    >>> hamming('hello', 'jelly')
    2

    >>> hamming('fun', 'ban')
    2

    >>> hamming('todd', 'john')
    3
    '''
    counter = 0
    for i in range(len(start)):
        if start[i] != end[i]:
            counter += 1
    return counter

def main(start, end, words = None):
    '''
    Reads the dictionary of words stored as a text file in the working directory,
    and creates a graph of words that equal the length of the start word.
    Calls the word ladder function to obtain the word ladder, and gives appropriate
    output based on the result.

    Arguments:
        start - start word
        end - end word
        words - word dictionary

    Returns:
        string - depends on whether a word ladder exists or not
    '''
    #getting,stripping, and lowercasing words from dictionary
    if words is None:
        words = set(word.strip().lower() for word in open("Dictionary.txt"))
    start = start.lower()
    end = end.lower()

    if len(start) != len(end):
        raise Exception("Words must be the same length.")

    #making sure end word can be accessed
    if end not in words:
        words.add(end)

    #creating graph object, and passing in dictionary and correct word length
    graph = Graph(words, len(start))

    #getting word path/ladder from start and end words
    word_ladder = graph.min_path(start, end)

    if word_ladder is None:
        return "No word ladder exists from " + start.upper() + " to " + end.upper()
    else:
        #making string for displaying path/ladder
        words = ""
        for i in word_ladder:
            words += i.upper() + " "
        return "Shortest Word Ladder: " + words

if __name__ == '__main__':
    def define_start_end(var, displaytext):
        '''
        This function is used to obtain the start and end values entered in
        the entry fields of the screen.
        '''

        start = start_word.get() # get start word
        end = end_word.get() # get end word
        ladder = main(start, end) # obtain shortest word ladder if it exists
        var.set(ladder) # letting path/ladder be displayed
        displaytext.grid(column=1, row=5)

    #setting up tkinter GUI pop-up
    screen = Tk()

    #Displaying Title
    label = Label(screen, text="WORD LADDER GENERATOR", anchor=CENTER, height=3, padx=10, pady=3)
    label.grid(column=1, row=0)
    
    #Displaying Start
    label1 = Label(screen, text="Start:")
    label1.grid(column=0, row=1)
    
    #entry spot for start_word
    start_word = Entry(screen, bd=5)
    start_word.grid(column=1, row=1)
    
    #displaying end
    label2 = Label(screen, text="End:")
    label2.grid(column=0, row=2)
    
    #entry spot for end_word
    end_word = Entry(screen, bd=5)
    end_word.grid(column=1, row=2)

    var = StringVar()
    displaytext = Label(screen, textvariable=var, anchor=CENTER, height=3)
    
    #creating button that links to function in main
    enterbutton = Button(screen, text="GO!", command= lambda:define_start_end(var, displaytext))
    enterbutton.grid(column=1, row=3)
    
    #keep updating to get new words and display new ladder
    screen.mainloop()
