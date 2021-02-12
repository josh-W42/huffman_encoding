import sys, heapq

def huffman_encoding(data):
    '''
    Compresses the data given by encoding it into binary by the huffman algorithm.

    Args:
        data(str): information to be compressed

    Returns:
        Encoded Data(str) of binary code.
        A tree generated from the huffman algorithm used to decode the binary.
    '''
    if type(data) != str:
        raise TypeError('param: data, needs to be of type str')
    elif len(data) == 0:
        raise ValueError('param: data, cannot be empty string')

    frequency = dict({})

    # step one, count the frequency 
    for item in data:
        if frequency.get(item):
            frequency[item]['frequency'] += 1
        else:
            frequency[item] = {'frequency': 1, 'huffman_code': None}

    # step two, create priority queue
    freq_list = list()

    for key, value  in zip(frequency.keys(), frequency.values()):
        new_node = Node(key, value['frequency'])
        freq_list.append(new_node)
    
    heapq.heapify(freq_list)

    # step three (going to be repeated) pop out two nodes with min freqeuncy (heapq.heappop)

    tree = Tree()

    # To handle single char inputs 
    if len(freq_list) == 1:
        freq_list[0].huffman_key = '0'

    while len(freq_list) >= 1:

        if len(freq_list) == 1:
            tree.set_root(freq_list[0])
            break
        else:
            left_node = heapq.heappop(freq_list)
            right_node = heapq.heappop(freq_list)

            # for step 6
            left_node.huffman_key = '0'
            right_node.huffman_key = '1'

    
            # step four (going to be repeated) create a new node wiht a freq = sum of the two nodes poped out
            #   This new node -> Huffman tree, and the two nodes would become the children. The lower frequency
            #   node becomes a left child, and the higher frequency node becomes the right child. Reinsert the
            #  newly created node back into the priority queue.

            new_val = left_node.freq + right_node.freq

            new_node = Node(new_val, new_val)
            new_node.prev = left_node
            new_node.next = right_node
            
            heapq.heappush(freq_list, new_node)


    

    # Phase 2

    #  traverese the tree,
    #  use the frequency dictionary to add in the huffman code
    #  Then finally translate the orginal data into a code

    for key in frequency.keys():
        frequency[key]['huffman_code'] = tree.huffman_code(key)

    final_encoding = ''

    for letter in data:
        final_encoding += frequency[letter]['huffman_code']

    return final_encoding, tree

def huffman_decoding(data, tree):
    '''
    Decodes the input data generated from the huffman algorithm

    Args:
        data(str): binary code in str data type form.
        tree(Tree): a tree generated from the huffman_encoding function
    
    Returns:
        The decoded data.
        An empty string if an error occured.
    '''
    if type(data) != str or type(tree) != Tree:
        raise TypeError('Requires data of type str and tree of type Tree')
    


    final_decoding = ''

    node = tree.get_root()
    index = 0
    while True:
        # For single character strings, there is only one node
        if node == tree.get_root() and (not node.has_left_node() or not node.has_right_node()):
            final_decoding += node.char
            index += 1
            if index == len(data):
                break
        elif type(node.char) == str:
            if final_decoding == '':
                final_decoding = node.char
            else:
                final_decoding += node.char
            # Reset the node whenever a character is encountered. Since all char nodes are leafs of the tree.
            node = tree.get_root()
        elif index == len(data):
            break
        elif data[index] == "0":
            node = node.prev
            index += 1
        elif data[index] == "1":
            node = node.next
            index += 1


    return final_decoding

class Node(object):
    def __init__(self, letter, freq):
        self.char = letter
        self.freq = freq
        self.prev = None
        self.next = None
        self.huffman_key = None

    def has_left_node(self):
        '''
        Checks if current node has left node

        Returns:
            True, if there is a left node
            False, Otherwise
        '''
        return not self.prev is None

    def has_right_node(self):
        '''
        Checks if current node has right node
        Returns:
            True, if there is a right node
            False, Otherwise
        '''
        return not self.next is None

    def get_left_node(self):
        '''
        Gets the left Node of current node

        Returns:
            Left node(Node) is it exists,
            None, otherwise
        '''
        if self.has_left_node:
            return self.prev
        else:
            return None
    
    def get_right_node(self):
        '''
        Gets the right Node of current node

        Returns:
            Right node(Node) is it exists,
            None, otherwise
        '''
        if self.has_right_node:
            return self.next
        else:
            return None

    def __lt__(self, other):
        return self.freq < other.freq
    
    def __gt__(self, other):
        return self.freq > other.freq


class Tree:
    def __init__(self):
        self.root = None

    def set_root(self, node):
        '''
        Sets the root node of the tree
        
        Args:
            node(Node): node
        '''
        self.root = node

    def get_root(self):
        '''
        Get the root of the Tree

        Returns:
            A (Node) object.'''
        return self.root

    def print(self):
        '''Prints the current tree to the console'''

        print("Printing Tree: \n")
        self.print_tree(self.root)

    def print_tree(self, root):
        '''
        Prints the tree to the console from the root.
        
        Args:
            root(Node): a root of a tree
        '''
        
        print('data:', root.char, root.freq)

        if root.has_left_node():
            print(root.char, "left")
            self.print_tree(root.get_left_node())
        if root.has_right_node():
            print(root.char, "right")
            self.print_tree(root.get_right_node())

    def huffman_code(self, key):
        '''
        Searches the tree for the key specified and generates a Huffman code for the path to the key.
        
        Args:
            key(str): A letter to be coded by huffman encoding.

        Returns:
            (str) string version of the Huffman code for a particular key within the tree.
            None  if no key is found.
        '''
        output = self.generate_code(key, self.root)
        return output[::-1]

    def generate_code(self, key, root):
        '''Helper function for the huffman_code method'''
        output = None

        if root.has_left_node():
            output = self.generate_code(key, root.get_left_node())
        if root.has_right_node() and output is None:
            output = self.generate_code(key, root.get_right_node())

        if root.char == key and not root.huffman_key is None:
            return root.huffman_key
        elif not output is None and not root.huffman_key is None:
            return output + root.huffman_key
        else:
            return output


''' Phase one, count the frequency of each !unique! character use 
    Ok so we need a doublely linked list queue//// NOPE JUST USE heapq  and minheap
    We may need a dictionary that contains information on the frequency of letters
    We need a tree/node structure!

    most likely O(n^2) worst case O(n log k) average case
'''

    



def test_suite():
    '''
    Performs a series of tests on the huffman_encoding and huffman_decoding functions
    '''
    print('\nBasic Function tests \n')

    print('Encoding Null Input Test: ', end=' ')
    try:
        huffman_encoding(None)
    except TypeError:
        print('pass')
    else:
        print('Fail')
    
    print('Enocoding Empty Input Test: ', end=' ')
    try:
        huffman_encoding('')
    except ValueError:
        print('pass')
    else:
        print('Fail')

    print('Decoding Null Input Test: ', end=' ')
    try:
        huffman_decoding(None, None)
    except TypeError:
        print('pass')
    else:
        print('Fail')

    
    print('\nFull Functionality Test: Single character strings: ')

    a_great_sentence = "aaa"

    print ("The size of the data is: {}\n".format(sys.getsizeof(a_great_sentence)))
    print ("The content of the data is: {}\n".format(a_great_sentence))

    encoded_data, tree = huffman_encoding(a_great_sentence)

    print ("The size of the encoded data is: {}\n".format(sys.getsizeof(int(encoded_data, base=2))))
    print ("The content of the encoded data is: {}\n".format(encoded_data))

    decoded_data = huffman_decoding(encoded_data, tree)

    print ("The size of the decoded data is: {}\n".format(sys.getsizeof(decoded_data)))
    print ("The content of the encoded data is: {}\n".format(decoded_data))

    print('Result: ', end=' ')
    if a_great_sentence == decoded_data:
        print('pass')
    else:
        print('Fail')
    
    print('\nFull Functionality Test:  w/ Test Sentence: ')

    a_great_sentence = "The bird is the word"

    print ("The size of the data is: {}\n".format(sys.getsizeof(a_great_sentence)))
    print ("The content of the data is: {}\n".format(a_great_sentence))

    encoded_data, tree = huffman_encoding(a_great_sentence)

    print ("The size of the encoded data is: {}\n".format(sys.getsizeof(int(encoded_data, base=2))))
    print ("The content of the encoded data is: {}\n".format(encoded_data))

    decoded_data = huffman_decoding(encoded_data, tree)

    print ("The size of the decoded data is: {}\n".format(sys.getsizeof(decoded_data)))
    print ("The content of the encoded data is: {}\n".format(decoded_data))

    print('Result: ', end=' ')
    if a_great_sentence == decoded_data:
        print('pass')
    else:
        print('Fail')
    

if __name__ == "__main__":
    codes = {}

    test_suite()
