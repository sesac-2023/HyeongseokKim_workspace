import random

for i in range(1000):
    year = random.randint(2019, 2022)
    month = random.randint(1, 12)
    day_max = 31
    if month == 2:
        day_max = 28
    elif month in [4, 6, 9, 11]:
        day_max = 30
    day = random.randint(1, day_max)

    hour = random.randint(1, 23)
    minute = random.randint(1, 59)
    seconds = random.randint(1, 59)

    target_file = f'./pdf_files/TEST_{year}-{month}-{day}_{hour}-{minute}-{seconds}.pdf'
    with open(target_file, 'w') as f:
        f.write(' ')
