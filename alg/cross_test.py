import random as rnd


class Elem:
    
    def __init__(self, key):
        self.key = key
        self.value = rnd.randint(1, 200)
        
    def __str__(self):
        return f"{self.key}/{self.value}"
        

first_test = [Elem(1),
              Elem(1),
              Elem(2),
              Elem(2),
              Elem(2),
              Elem(3),
              Elem(4),
              Elem(4),
              Elem(4),
              Elem(4),
              Elem(5)]

first_dict = {
    1:2,
    2:3,
    3:1,
    4:4,
    5:1
}

second_test =[Elem(1),
              Elem(1),
              Elem(1),
              Elem(1),
              Elem(2),
              Elem(3),
              Elem(3),
              Elem(3),
              Elem(4),
              Elem(5),
              Elem(5)]

second_dict = {
    1:4,
    2:1,
    3:3,
    4:1,
    5:2
}

first_tasks = list(first_dict.values())
second_tasks = list(second_dict.values())

child_1 = first_test.copy()
child_2 = second_test.copy()
for i in range(5):
    start_index_1 = sum(first_tasks[:i])
    start_index_2 = sum(second_tasks[:i])
    
    if first_tasks[i] > second_tasks[i]:
        ones = [1 for _ in range(second_tasks[i])]
        zeros = [0 for _ in range(first_tasks[i] - second_tasks[i])]
        ones.extend(zeros)
        mask = ones
        rnd.shuffle(mask)
        for i, e in enumerate(mask):
            if e == 1:
                child_1[start_index_1 + i], child_2[start_index_2] = child_2[start_index_2], child_1[start_index_1 + i]
                start_index_2 += 1
                
    elif first_tasks[i] < second_tasks[i]:
        ones = [1 for _ in range(first_tasks[i])]
        zeros = [0 for _ in range(second_tasks[i] - first_tasks[i])]
        ones.extend(zeros)
        mask = ones
        rnd.shuffle(mask)
        for i, e in enumerate(mask):
            if e == 1:
                child_2[start_index_2 + i], child_1[start_index_1] = child_1[start_index_1], child_2[start_index_2 + i]
                start_index_1 += 1
        
    else:
        if first_tasks[i] > 1:
            ones = [1 for _ in range(first_tasks[i] // 2)]
            zeros = [0 for _ in range(second_tasks[i] - first_tasks[i] // 2)]
            ones.extend(zeros)
            mask = ones
            rnd.shuffle(mask)
            for i, e in enumerate(mask):
                if e == 1:
                    child_1[start_index_1 + i], child_2[start_index_2 + i] = child_2[start_index_2 +i], child_1[start_index_1 + i]
                    
                    
print('Первый родитель:')
for t in first_test:
    print(t)
print()

print('Второй родитель:')
for t in second_test:
    print(t)
print()

print('Первый ребенок:')
for t in child_1:
    print(t)
print()

print('Второй ребенок:')
for t in child_2:
    print(t)
print()