import random


def choose_candidates(population, t):
    indexes = []
    while len(indexes) != t:
        new_index = max(round(random.random() * len(population)-1), 0)
        if new_index not in indexes:
            indexes.append(new_index)
    return [population[i] for i in indexes]


class Selection:
    def select_parents_pool(self, population_with_health):
        raise NotImplementedError


class TournamentWithReturnSelection(Selection):
    def __init__(self, p):
        self.name = f"tournament_with_return_p_{p}"
        self.p = p

    def select_parents_pool(self, population_with_health):
        """
        population_with_health [(candidate, health_fun(candidate))]
        t (number of candidates) == 2
        """
        n = len(population_with_health)
        new_population = []
        while len(new_population) != n:
            candidates = choose_candidates(population_with_health, 2)
            if random.random() <= self.p:
                rate = sorted(candidates, key=lambda tup: tup[1], reverse=True)
            else:
                rate = sorted(candidates, key=lambda tup: tup[1])
            new_population.append(rate[0])
        return new_population


class TournamentWithoutReturnSelection(Selection):
    def __init__(self, p):
        self.name = f"tournament_without_return_p_{p}"
        self.p = p

    def select_parents_pool(self, population_with_health):
        """
        population_with_health [(candidate, health_fun(candidate))]
        t (number of candidates) == 2
        """
        # as t == 2, make 2 copy of population
        second_copy = population_with_health.copy()
        current_population = population_with_health
        n = len(population_with_health)
        new_population = []
        while len(new_population) != n:
            # todo fix for odd number
            if len(current_population) < 2:
                current_population = second_copy
            candidates = choose_candidates(current_population, 2)
            for c in candidates:
                current_population.remove(c)
            if random.random() <= self.p:
                rate = sorted(candidates, key=lambda tup: tup[1], reverse=True)
            else:
                rate = sorted(candidates, key=lambda tup: tup[1])
            new_population.append(rate[0])

        return new_population


class LinearRankingSelection(Selection):
    def __init__(self, b):
        self.name = f"linear_ranking_selection_b_{b}"
        self.b = b

    def calc_ranking(self, population):
        sorted_population = sorted(population, key=lambda tup: tup[1])
        population_with_ranking = [(sorted_population[i][0], sorted_population[i][1], i) for i in range(len(sorted_population))]
        return population_with_ranking[::-1]

    def p_linear_rank(self, value, N):
        return (2-self.b)/N + (2 * value * (self.b-1))/(N*(N-1))

    def calc_p(self, population):
        ranking_population = self.calc_ranking(population)
        N = len(ranking_population)
        res = []
        prev_val = 0
        for i in ranking_population:
            p = self.p_linear_rank(i[2], N)
            new_val = prev_val + p
            res.append((i[0], i[1], (prev_val, new_val)))
            prev_val = new_val
        return res

    def select_parents_pool(self, population_with_health):
        population_with_p_values = self.calc_p(population_with_health)
        n = len(population_with_health)
        step = 1 / n

        def get_item_by_sus_position(sus_position):
            # todo optimize
            for i in range(n):
                if population_with_p_values[i][2][0] <= sus_position < population_with_p_values[i][2][1]:
                    return (population_with_p_values[i][0], population_with_p_values[i][1])

        current_position = random.random()
        new_population = []
        while len(new_population) != n:
            new_population.append(get_item_by_sus_position(current_position))
            new_pos = current_position + step
            current_position = new_pos if new_pos < 1 else new_pos - 1
        return new_population