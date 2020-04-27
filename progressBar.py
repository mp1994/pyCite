import time
import sys

'''
    Progress Bar
    Parameters: width = number of iterations
'''

class progressBar():

    ''' Init function '''
    def __init__(self, width):
        if width is None:
            self.width = 40
        else:
            self.width = width

        sys.stdout.write("[%s]" % (" " * self.width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (self.width+1)) # return to start of line, after '['
        
        self.iter = 0
            
    ''' Update function > use this inside for loops '''
    def update(self):
        sys.stdout.write("-")
        sys.stdout.flush()
        
        self.iter = self.iter + 1
        
        if self.iter == self.width:
            sys.stdout.write("]\n") # this ends the progress bar
        

if __name__ == '__main__':

    pBar = progressBar(40)

    for i in range(pBar.width):
        time.sleep(0.1) # do real work here
        # update the bar
        pBar.update()