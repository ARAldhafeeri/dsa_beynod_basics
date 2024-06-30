def build_suffix_array(s):
	 # Get the length of the string
    n = len(s)
    
    # Initialize the suffix array with indices of the string
    suffix_array = list(range(n))
    
    # Initialize the rank array with ASCII values of characters in the string
    rank = [ord(c) for c in s]
    
    # Start with a comparison length of 1
    k = 1

    # Define a function to create the key for sorting the suffixes
    def key(i):
        # The key is a tuple of the current rank and the rank of the suffix starting k positions ahead
        return (rank[i], rank[i + k] if i + k < n else -1)

    # Loop until the comparison length k is less than the string length
    while k < n:
        # Sort the suffix array based on the key
        suffix_array.sort(key=key)
        
        # Initialize a new rank array
        new_rank = [0] * n
        
        # Assign new ranks based on the sorted order
        for i in range(1, n):
            new_rank[suffix_array[i]] = new_rank[suffix_array[i - 1]]
            if key(suffix_array[i]) > key(suffix_array[i - 1]):
                new_rank[suffix_array[i]] += 1
        
        # Update the rank array
        rank = new_rank
        # Double the comparison length
        k *= 2
        print("end", k, suffix_array, rank)



    # Return the constructed suffix array
    return suffix_array

def search(pat, txt, suffArr, n):
   
    # Get the length of the pattern
    m = len(pat)
     
    # Initialize left and right indexes
    l = 0
    r = n-1
     
    # Do simple binary search for the pat in txt using the built suffix array
    while l <= r:
       
        # Find the middle index of the current subarray
        mid = l + (r - l)//2
         
        # Get the substring of txt starting from suffArr[mid] and of length m
        res = txt[suffArr[mid]:suffArr[mid]+m]
         
        # If the substring is equal to the pattern
        if res == pat:
           
            # Print the index and return
            print("Pattern found at index", suffArr[mid])
            return
           
        # If the substring is less than the pattern
        if res < pat:
           
            # Move to the right half of the subarray
            l = mid + 1
        else:
           
            # Move to the left half of the subarray
            r = mid - 1
            
            
s = "banana"
suffix_array = build_suffix_array(s)
print(suffix_array)  # Output: [5, 3, 1, 0, 4, 2]

