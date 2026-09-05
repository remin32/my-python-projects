candidates = ["Иванов", "Петров", "Сидорова"]
votes = {"Иванов": 0, "Петров": 0, "Сидорова": 0}
print("_______ГОЛОСОВАНИЕ_______")
quantity=int(input("Сколько будет голосующих?: "))
for i in range(quantity):
    print("\nКандидаты: " + str(candidates))
    vote= input("За кого голосуешь(фамилия)?: ")
    if vote in candidates:
        if vote == candidates[0]:
            votes[vote] += 1
        elif vote == candidates[1]:
            votes[vote] += 1
        elif vote == candidates[2]:
            votes[vote] += 1 
        print("Вы успешно проголовали!")
    else:
        print("Такого кандитата нет! Ваш голос не защитывается")
sort = sorted(votes.items(), key =lambda item: item[1], reverse= True)
print("\n\n")
for s in sort:
    print(s[0] + ": " + str(s[1]) + " голосов(а)")
if sort[0][1] == sort[1][1]:
    print("Нужны перевыборы! ")
else:   
    best_name = sort[0][0]
    best_votes = sort[0][1]
    print("Лучший кандидат -- " + best_name + ": " + str(best_votes) + " голосов")
cd путь_к_проекту
git init
git add .
git commit -m "мой первый коммит"