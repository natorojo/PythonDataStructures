class PriorityQ:
    def __init__(self):
        """
            priority Q based on min heap

            Todo: incorporate typing. 
            Todo: more general min/max heap (ie allow both heap types)

            note: only supports keys of type int/string/tuple(int or string)
        """
        self._heap = [] #: List[int]

        #a map from key to heap index
        #this is used internally for removing items
        #and changing priorities of items
        #note: keys MUST be UNIQUE
        self._keys = {} #: Dict[int or str or tuple(int or str),int]

        #a map from heap indices to keys
        #this is used to extract/get next
        self._priorities = {}

    def _parent(self,i):
        return int((i-1)/2)

    def _left_child(self,i):
        return 2*i + 1

    def _right_child(self,i):
        return 2*i + 2

    def _update_maps(self,a,b):
        #update maps
        #get keys using priorites
        keya = self._priorities[a]
        keyb = self._priorities[b]

        #do swaps
        self._keys[keya] = b
        self._keys[keyb] = a 

        self._priorities[a] = keyb
        self._priorities[b] = keya

    def _sift_down(self,i):
        """
            this is an implementation of sift down that
            maintains
        """
        minIndex = i
        size = len(self._heap)

        #--------------------------------------------------------------------
        #check which child (if any) should be swapped with item at i
        #--------------------------------------------------------------------
        #check if left child violates min heap
        #property
        l = self._left_child(i)
        if l < size and self._heap[l] < self._heap[minIndex]:
            minIndex = l

        #check if right child violates min heap
        #property
        r = self._right_child(i)
        if r < size and self._heap[r] < self._heap[minIndex]:
            minIndex = r

        #--------------------------------------------------------------------
        #if we found a violation do swap and recur
        #and update keys map
        #--------------------------------------------------------------------    
        if i != minIndex:
            #swap priorities in the heap
            self._heap[i], self._heap[minIndex] = self._heap[minIndex], self._heap[i]

            #update keys map: this MUST be before the recursion
            self._update_maps(i,minIndex)

            #recursively sift
            self._sift_down(minIndex)

    def _sift_up(self,i):
        p = self._parent(i)
        #note int(-1/2) == 0
        #so the root will never violate min heap property
        #a violation do swap and recur
        if self._heap[i] < self._heap[p]:
            #swap:
            self._heap[i], self._heap[p] = self._heap[p], self._heap[i]


            #update maps
            self._update_maps(i,p)

            #recur:
            self._sift_up(p)

    def insert(self,priority,key):
        #check for uniqueness
        assert key not in self._keys.keys(), 'keys MUST be UNIQUE'
        size = len(self._heap)
        self._keys[key] = size
        self._priorities[size] = key
        self._heap.append(priority)
        self._sift_up(size)

    def next(self):
        """
            returns the next item without altering q
        """
        return self._priorities[0]

    def extract(self):
        """
            returns next item and removes it from q
        """
        extracted_key = self._priorities[0]
        size = len(self._heap)
        #swap last and first priorities
        self._heap[0],self._heap[size-1] = self._heap[size-1],self._heap[0]
        #update maps to reflect this
        self._update_maps(0,size - 1)
        
        #remove old min
        self._heap.pop()
        del self._keys[extracted_key]
        del self._priorities[size-1]

        #sift_down
        self._sift_down(0)
        return extracted_key

    def change_priority(self, key, new_priority):
        #get idx of priority from key
        heap_idx = self._keys[key]
        #get old priority
        prev_priority = self._heap[heap_idx]
        if new_priority != prev_priority:
            #set new priority
            self._heap[heap_idx] = new_priority
            #do sifting
            if new_priority < prev_priority:
                #mean heaps sift lesser items ups
                self._sift_up(heap_idx)
            else:
                #mean heaps sift greater items down
                self._sift_down(heap_idx)

    def empty(self):
        return len(self._heap) == 0

    def debug(self):
        print(self._heap)
        print(self._keys)
        print(self._priorities)
