"""
A script which simulates the bidirectional transformation process.

Authors: Daniel Cowan and John Morphett
"""
import random
from pandas import DataFrame

"""
This class represents a 1-BT, or a tournament which contains 1 bidirectional arc.
"""


class Tournament:
    def __init__(self):
        self.nodes = []
        self.bidirectional_arc = []
        self.removed = []
        self.list_num_arcs = []

    # string representation of the tournament; uses the in-degree of each node
    def __str__(self):
        string = ""

        for node in self.nodes:
            if node.name in self.removed:
                continue

            string += node.name + ": " + repr(node.in_degree) + "\n"

        return string

    # creates a random tournament
    # num_nodes = the size of the tournament
    def initialize_tournament(self, num_nodes):

        # boolean which is True if the tournament contains a bidirectional arc
        contains_bi = False

        # initialize the node objects
        for i in range(num_nodes):
            new_node = Node(i)
            self.nodes.append(new_node)

        # create random connections between the nodes
        for i in range(num_nodes-1):
            for j in range(i+1, num_nodes):

                # make sure the tournament doesn't already have a bidirectional arc
                if not contains_bi:
                    rand_int = random.randint(0, 2)

                else:
                    rand_int = random.randint(0, 1)

                if rand_int == 0:
                    self.nodes[i].out_degree.add(self.nodes[j].name)
                    self.nodes[j].in_degree.add(self.nodes[i].name)

                if rand_int == 1:
                    self.nodes[i].in_degree.add(self.nodes[j].name)
                    self.nodes[j].out_degree.add(self.nodes[i].name)

                if rand_int == 2:
                    self.nodes[i].out_degree.add(self.nodes[j].name)
                    self.nodes[i].in_degree.add(self.nodes[j].name)

                    self.nodes[j].out_degree.add(self.nodes[i].name)
                    self.nodes[j].in_degree.add(self.nodes[i].name)

                    self.bidirectional_arc.append(i)
                    self.bidirectional_arc.append(j)

                    contains_bi = True

        # if we've created all the connections and there's no bidirectional arc,
        # then randomly choose a place to put the arc
        if not contains_bi:
            rand_i = random.randint(0, num_nodes-1)
            rand_j = random.randint(0, num_nodes-1)

            # make sure we're selecting different nodes
            while rand_i == rand_j:
                rand_i = random.randint(0, num_nodes-1)
                rand_j = random.randint(0, num_nodes-1)

            self.nodes[rand_i].out_degree.add(self.nodes[rand_j].name)

            self.nodes[rand_i].in_degree.add(self.nodes[rand_j].name)

            self.nodes[rand_j].out_degree.add(self.nodes[rand_i].name)

            self.nodes[rand_j].in_degree.add(self.nodes[rand_i].name)

            # has to do with how we chose to order the bidirectional_arc list
            if rand_i < rand_j:
                self.bidirectional_arc.append(rand_i)
                self.bidirectional_arc.append(rand_j)
            else:
                self.bidirectional_arc.append(rand_j)
                self.bidirectional_arc.append(rand_i)

    # this method handles the bidirectional transformation process
    def transformation(self):
        iterations = 0

        # continue as long as we have a bidirectional arc and more than 2 nodes
        while len(self.bidirectional_arc) > 0 and (len(self.nodes) - len(self.removed) > 2):
            iterations += 1

            self.list_num_arcs.append(int(len(self.bidirectional_arc) / 2))

            bidir_i = self.bidirectional_arc.pop(0)
            bidir_j = self.bidirectional_arc.pop(0)

            self.bidirectional_arc = []

            self.removed.append(str(bidir_i))
            self.removed.append(str(bidir_j))

            new_base_node = Node(len(self.nodes))

            # update connections
            for node in self.nodes:
                if node.name in self.removed:
                    continue

                if str(bidir_i) in node.in_degree:
                    node.in_degree.remove(str(bidir_i))

                if str(bidir_j) in node.in_degree:
                    node.in_degree.remove(str(bidir_j))

                if str(bidir_i) in node.out_degree:
                    node.out_degree.remove(str(bidir_i))

                if str(bidir_j) in node.out_degree:
                    node.out_degree.remove(str(bidir_j))

                if node.name in self.nodes[bidir_i].in_degree and node.name in self.nodes[bidir_j].in_degree \
                        and not (node.name in self.nodes[bidir_i].out_degree or node.name in self.nodes[bidir_j].out_degree):
                    new_base_node.in_degree.add(node.name)
                    node.out_degree.add(new_base_node.name)

                elif node.name in self.nodes[bidir_i].out_degree and node.name in self.nodes[bidir_j].out_degree \
                        and not (node.name in self.nodes[bidir_i].in_degree or node.name in self.nodes[bidir_j].in_degree):
                    new_base_node.out_degree.add(node.name)
                    node.in_degree.add(new_base_node.name)

                else:
                    self.bidirectional_arc.append(int(node.name))
                    self.bidirectional_arc.append(
                        len(self.nodes))

                    new_base_node.out_degree.add(node.name)
                    new_base_node.in_degree.add(node.name)

                    node.out_degree.add(new_base_node.name)
                    node.in_degree.add(new_base_node.name)

            self.nodes.append(new_base_node)

        self.list_num_arcs.append(int(len(self.bidirectional_arc) / 2))

        return iterations


# this class represents a node in a tournament
class Node:
    def __init__(self, i):
        self.in_degree = set()
        self.out_degree = set()
        self.name = str(i)


def main():

    run = input(
        "Run 1 tournament (input 'one') or an average of many tournaments (input 'avg')? ")

    while not (run == "one" or run == "avg"):
        print("Please input 'one' or 'avg'.")

        run = input(
            "Run 1 tournament (input 'one') or an average of many tournaments (input 'avg')? ")

    if run == 'one':
        t_size = int(input("What do you want the tournament size to be? "))
        its = int(input("How many iterations? "))

        avg_its = 0.0
        arcs = []

        for i in range(its):
            tournament = Tournament()
            tournament.initialize_tournament(t_size)
            avg_its += tournament.transformation()
            arcs.append(tournament.list_num_arcs)

        avg = []
        max_len = 0

        for i in range(len(arcs)):
            if len(arcs[i]) > max_len:
                max_len = len(arcs[i])

        for i in range(max_len):
            avg.append(0)

        for i in range(len(arcs)):
            for j in range(max_len):
                try:
                    avg[j] += arcs[i][j]

                except:
                    avg[j] += 0

        avg = [i/its for i in avg]

        print("On average - for tournament of size", t_size, "- we saw:")

        for i in range(len(avg)):
            print(avg[i], "bidirectional arcs after", i, "transformations")

        avg_its = avg_its / its

        print("For tournament of size", t_size,
              "the transformation process averaged", avg_its, "steps.")

    else:

        max_t_size = int(input("Max tournament size? "))

        while max_t_size < 3:
            print("Max tournament size must be greater than 3. Try again.")
            max_t_size = int(input("Max tournament size? "))

        its = int(input("Number of iterations per tournament size? "))

        res_dict = {"iterations": [], "tournament_size": [],
                    "exp_transformation_steps": [], "step": [], "expected_arcs": []}

        for it in range(3, max_t_size + 1):
            arcs = []
            avg_its = 0
            t_size = it

            for i in range(its):
                tournament = Tournament()
                tournament.initialize_tournament(t_size)
                avg_its += tournament.transformation()
                arcs.append(tournament.list_num_arcs)

            avg = []
            avg_its /= its

            max_len = 0

            for i in range(len(arcs)):
                if len(arcs[i]) > max_len:
                    max_len = len(arcs[i])

            for i in range(max_len):
                avg.append(0)

            for i in range(len(arcs)):
                for j in range(max_len):
                    try:
                        avg[j] += arcs[i][j]

                    except:
                        avg[j] += 0

            avg = [i/its for i in avg]

            print("On average - for tournament of size", t_size, "- we expect:")

            for i in range(len(avg)):
                print(avg[i], "bidirectional arcs after", i, "transformations")
                res_dict["iterations"].append(its)
                res_dict["tournament_size"].append(t_size)
                res_dict["exp_transformation_steps"].append(avg_its)
                res_dict["step"].append(i)
                res_dict["expected_arcs"].append(avg[i])

        df = DataFrame(res_dict)
        df.to_csv("results_3_to_" + str(max_t_size) + ".csv")


if __name__ == "__main__":
    main()
