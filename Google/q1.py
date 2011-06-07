from sys import stdin

def solver(packets):
    pos = [1,1]
    time = [0,0]
    name = {'O' : 0 , 'B' : 1}
    last = 0
    for (n,d) in packets:
        idx = name[n] #determine which robo
        dest = int(d) #where is it going
        trav = abs(dest - pos[idx])#travel time
        time[idx] += trav #add this to the robot's travel
        pos[idx] = dest
        #last = time pressed -> max of now or last move + 1 (press time)
        last = time[idx] = max(time[idx],last) + 1 #
    return last


if __name__ == '__main__':
    
    count = int(stdin.readline())
    for c in xrange(1,count+1): #for the number of cases
        line = stdin.readline()
        ll = line.split()[1:] #split by space, drop the first value
        #msgs = zip(ll[1::2],ll[2::2]) #start:end:stepsize2
        msgs = [ (ll[i], ll[i+1]) for i in xrange(0,len(ll),2)] #more efficient
        print "Case #{0}: {1}".format(c,solver(msgs)) # % () is being dep
