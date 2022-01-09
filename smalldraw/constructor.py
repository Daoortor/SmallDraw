from drawing.models import Word, Category


raw = open('words.txt').read()
categories = {category.split()[0]: (int(category.split()[1]), category.split()[2:]) for category in raw.split('\n\n')}
print(categories)
for cat_name in categories.keys():
    Category.objects.get_or_create(name=cat_name, points=categories[cat_name][0])
    cat = Category.objects.get(name=cat_name)
    for word in categories[cat_name][1]:
        Word.objects.get_or_create(word=word, category_id_id=cat.id)
