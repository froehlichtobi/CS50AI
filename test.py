import random

pages = ['1.html', '2.html', '3.html']
probabilities = [0.475, 0.475, 0.05]
n1, n2, n3 = 0,0,0
for i in range(1000):
    selected_page = random.choices(pages, weights=probabilities)[0]
    if(selected_page) == '1.html':
        n1 += 1
    elif(selected_page) == '2.html':
        n2 += 1
    elif(selected_page) == '3.html':
        n3 += 1

    print(selected_page)
print(n1, n2, n3)
