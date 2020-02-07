from __future__ import print_function
from collections import namedtuple
from ortools.sat.python import cp_model


class HeroesPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, classes, classOrigin, heroes, num_heroes, num_slots, num_classes, sols):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._classes = classes
        self._classOrigin = classOrigin
        self._heroes = heroes
        self._num_heroes = num_heroes
        self._num_slots = num_slots
        self._num_classes = num_classes
        self._solutions = set(sols)
        self._solution_count = 0

    def on_solution_callback(self):
        if self._solution_count in self._solutions:
            print('Solution %i' % self._solution_count)
            for s in range(self._num_slots):
                print('Slot %i' % s)
                for n in range(self._num_heroes):
                    is_working = False
                    # for s in range(self._num_classes):
                    if self.Value(self._classes[(n, s)]):
                        is_working = True
                        print('  Hero %s works class %i' % (self._heroes[n][0], s))
                        # print('  Hero %s works class %s' % (self._heroes[n][0], self._classOrigin[s]))
                    if not is_working:
                        print('  Hero {} does not work'.format(n))
            print()
        self._solution_count += 1

    def solution_count(self):
        return self._solution_count


def main():
    # This program tries to find an optimal assignment of Heroes to classes
    # (3 classes per slot, for 7 slots), subject to some constraints (see below).
    # Each Hero can request to be assigned to specific classes.
    # The optimal assignment maximizes the number of fulfilled class requests.
    classOrigin = [
        # 'Alchemist', 'Assassin', 'Avatar',
        'Berserker', 'Blademaster', 'Mage',  'Desert',  'Electric',  'Glacial',  'Inferno',  'Light', 'Mystic',  'Ocean',  'Poison',  'Shadow', 'Wind'
        # , 'Druid'
        #    'Mystic', 'Predator', 'Ranger', 'Soulbound', 'Summoner', 'Warden'
    ]
    heroes = [['Renekton', 'Berserker', 'Desert'], ['Volibear', 'Berserker', 'Electric', 'Glacial'], ['Olaf', 'Berserker', 'Glacial'],
              ['Jax', 'Berserker', 'Light'], ['DrMundo', 'Berserker', 'Poison'], ['Sion', 'Berserker', 'Shadow'], ['Sivir', 'Blademaster', 'Desert'],
              ['Aatrox', 'Blademaster', 'Light'], ['MasterYi', 'Blademaster', 'Mystic', 'Shadow'], ['Yasuo', 'Blademaster', 'Wind'], ['Brand',
              'Mage', 'Inferno'], ['Veigar', 'Mage', 'Shadow'], ['Syndra', 'Mage', 'Ocean'],
              ['Vladimir', 'Mage', 'Ocean']
              ]
    
    print(heroes[1][0])
    # print(classOrigin[heroes[1][1]])
    num_heroes = len(heroes)
    num_classes = len(classOrigin)
    print(num_classes)
    num_slots = 5
    all_heroes = range(num_heroes)
    all_classes = range(num_classes)
    all_slots = range(num_slots)
    class_requests = [[[0, 0, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 1],
                       [0, 1, 0], [0, 0, 1]],
                      [[0, 0, 0], [0, 0, 0], [0, 1, 0], [0, 1, 0], [1, 0, 0],
                       [0, 0, 0], [0, 0, 1]],
                      [[0, 1, 0], [0, 1, 0], [0, 0, 0], [1, 0, 0], [0, 0, 0],
                       [0, 1, 0], [0, 0, 0]],
                      [[0, 0, 1], [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 0],
                       [1, 0, 0], [0, 0, 0]],
                      [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 0], [1, 0, 0],
                       [0, 1, 0], [0, 0, 0]]]
    # Creates the model.
    model = cp_model.CpModel()

    # Creates class variables.
    # classes[(n, d, s)]: Hero 'n' works class 's' on slot 'd'.
    classes = {}
    for n in heroes[0:]:
        for c in n[1:]:
            for s in all_slots:
                # print(('class_n%sc%ss%i' % (n[0], c, s)))
                classes[(heroes.index(n), classOrigin.index(c), s)] = model.NewBoolVar('class_n%sc%ss%i' % (n[0], c, s))
                print(classes[(heroes.index(n), classOrigin.index(c), s)])
    # for n in all_heroes:
    #     for d in all_slots:
    #         for s in all_classes:
    #             classes[(n, d,
    #                      s)] = model.NewBoolVar('class_n%id%is%i' % (n, d, s))

    # Each class is assigned to exactly one Hero in .
    for s in all_slots:
        # print(classes[(heroes.index(n), classOrigin.index(c), s)] for n in heroes[0:] for c in n[1:])
        model.Add(sum(classes[(heroes.index(n), classOrigin.index(c), s)] for n in heroes[0:] for c in n[1:] )  == 1)

    # Each Hero works at most one class per slot.
    for n in heroes[0:]:
        for c in n[1:]:
            model.Add(sum(classes[(heroes.index(n), classOrigin.index(c), s)] for s in all_slots) <= 1)

    # min_classes_assigned is the largest integer such that every Hero can be
    # assigned at least that number of classes.
    # min_classes_per_hero = (num_classes * num_slots) // num_heroes
    # max_classes_per_hero = min_classes_per_hero + 1
    # for n in all_heroes:
    #     num_classes_worked = sum(
    #         classes[(n, d, s)] for d in all_slots for s in all_classes)
    #     model.Add(min_classes_per_hero <= num_classes_worked)
    #     model.Add(num_classes_worked <= max_classes_per_hero)

    # for n in all_heroes:
    #     num_classes_worked = sum(
    #         classes[(n, s)] for s in all_slots)
    #     model.Add(1 <= num_classes_worked)
    #     model.Add(num_classes_worked <= 1)
     # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0
    # Display the first five solutions.
    a_few_solutions = range(2)
    solution_printer = HeroesPartialSolutionPrinter(classes, classOrigin, heroes, num_heroes,
                                                    num_slots, num_classes,
                                                    a_few_solutions)
    solver.SearchForAllSolutions(model, solution_printer)

    # Statistics.
    print()
    print('Statistics')
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f s' % solver.WallTime())
    print('  - solutions found : %i' % solution_printer.solution_count())

    # model.Maximize(
    #     sum(class_requests[n][d][s] * classes[(n, d, s)] for n in all_heroes
    #         for d in all_slots for s in all_classes))
    # Creates the solver and solve.
    # solver = cp_model.CpSolver()
    # solver.Solve(model)
    # for d in all_slots:
    #     print('slot', d)
    #     for n in all_heroes:
    #         for s in all_classes:
    # if solver.Value(classes[(n, d, s)]) == 1:
    #     if class_requests[n][d][s] == 1:
    #         print('Hero', n, 'works class', s, '(requested).')
    #     else:
    #         print('Hero', n, 'works class', s, '(not requested).')
    # print()

    # Statistics.
    # print()
    # print('Statistics')
    # print('  - Number of class requests met = %i' % solver.ObjectiveValue(),
    #       '(out of', num_heroes * min_classes_per_Hero, ')')
    # print('  - wall time       : %f s' % solver.WallTime())


if __name__ == '__main__':
    main()
