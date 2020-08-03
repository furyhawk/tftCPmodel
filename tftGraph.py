class Champion(object):
    def __init__(self, json):
        """
        Creating champion object from JSON data.
        """
        self.id = json['id']
        self.key_ = json['key'].lower() # name
        self.name = json['name']
        self.origin1 = json['origin'] # Array of 2 at most
        self.origin2 = None # Not all Champs have 2 Origins
        self.class1 = json['class'] # Array of 2 at most
        self.class2 = None # Not all Champs have 2 Classes
        self.cost = json['cost']
        self.ability = json['ability']
        self.stats = json['stats']
        self.items = json['items']
        self.classes = []

        # Adjusting for characters with more than one class or origin attributes.
        if len(self.origin1) > 1:
            self.origin2 = self.origin1[1].lower()
            self.origin1 = self.origin1[0].lower()
            # self.classes + [self.origin1, self.origin2]
            self.classes.append(self.origin1)
            self.classes.append(self.origin2)

        else:
            self.origin1 = self.origin1[0].lower()
            self.classes.append(self.origin1)

        if len(self.class1) > 1:
            self.class2 = self.class1[1].lower()
            self.class1 = self.class1[0].lower()
            # self.classes + [self.class2, self.class1]
            self.classes.append(self.class2)
            self.classes.append(self.class1)

        else:
            self.class1 = self.class1[0].lower()
            self.classes.append(self.class1)

def _add_edges(self):
        """
        Given the graph with all the champions, add edges to connect people of the same class.
        Runtime: O(n^3) Probably even worse because of graph.AddEdge.
        """
        for class_ in self.champions_in_class.keys(): # For each class
            for champ in self.champions_in_class[class_]: # For each Champ of that class
                for champ_of_same_class in self.champions_in_class[class_]: # Loop to all the other champions of the same class.
                    if champ != champ_of_same_class: # Don't connect to itself
                        # print("Champ 1: {}, Champ 2: {}".format(champ,champ_of_same_class))
                        self.graph.addEdge(fromVert=champ, toVert=champ_of_same_class) # Connect Champ and all the champs of same class.

def find_all_champs_same_class_as(self, vert):
        """
        Find all champs for each champ class in vert.champ
        Runtime: O(3) * O(51) * (O(3) + O(3) + (O(5) * O(7)) = O(6273)
        """
        start = self.getVertex(vert) # Root

        checked_classes = set()
        array_of_champs = {} # { 'yordle': set('kennen', ...), ...}

        # print("All of {}'s classes: {}".format(vert, start.champ.classes))
        print("\n{}'s classes are: {}\n".format(vert.upper(), start.champ.classes))

        for class_ in start.champ.classes: # O(3) Worst Case
            if class_ != None:
                # print("Checking {} class".format(class_))
                vertices = set(self.getVertices())

                clique = set()
                clique.add(start)

                for vertex in vertices - clique: # O(51) Worst
                    # print("Comparing {} to {}".format(vert, vertex))
                    if class_ in vertex.champ.classes: # O(3) Worse
                        matching_classes = set(start.champ.classes).intersection(set(vertex.champ.classes))
                        has_unchecked_match = False

                        for match in matching_classes: # O(3) Worse
                            if match not in checked_classes:
                                has_unchecked_match = True
                                # print("{} matches to {} by {} class".format(vertex, vert, match))

                        if has_unchecked_match == True:
                            neighbor_of_all = True
                            for v in clique: # O(5) Worse
                                if vertex not in v.get_neighbors(): # O(7) Worse
                                    # print("Vertex {} and Vertex {} are not neighbors".format(vertex, v))
                                    neighbor_of_all = False
                            if neighbor_of_all == True:
                                clique.add(vertex)

                array_of_champs[class_] = clique # O(1)
        return array_of_champs