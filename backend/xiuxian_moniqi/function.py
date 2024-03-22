import random

from app_item.models import Item, Book

# function

def f_addItemtoBag(bag, item):
    try:
        bag.items[str(item.id)] += 1
    except:
        bag.items[str(item.id)] = 1
    bag.save()


def f_removeItemfromBag(bag, item):
    try:
        bag.items[str(item.id)] -= 1
        if bag.items[str(item.id)] <= 0:
            del bag.items[str(item.id)]
    except:
        del bag.items[str(item.id)]
    bag.save()


def f_addBooktoBag(bag, item):
    try:
        bag.books[str(item.id)] += 1
    except:
        bag.books[str(item.id)] = 1
    bag.save()


def f_removeBookfromBag(bag, item):
    try:
        bag.books[str(item.id)] -= 1
        if bag.books[str(item.id)] <= 0:
            del bag.books[str(item.id)]
    except:
        del bag.books[str(item.id)]
    bag.save()


def f_addSeedtoStore(house, seed):
    try:
        house.store[str(seed.id)] += 1
    except:
        house.store[str(seed.id)] = 1
    house.save()


def f_removeSeedtoStore(house, seed):
    try:
        house.store[str(seed.id)] -= 1
        if house.store[str(seed.id)] <= 0:
            del house.store[str(seed.id)]
    except:
        del house.store[str(seed.id)]
    house.save()


def f_getRandomItem(type):
    number = random.randint(0, 2048)
    if number == 1:
        quality = 10
    elif 1 < number <= 4:
        quality = 9
    elif 4 < number <= 9:
        quality = 8
    elif 9 < number <= 19:
        quality = 7
    elif 19 < number <= 50:
        quality = 6
    elif 50 < number <= 100:
        quality = 5
    elif 100 < number <= 200:
        quality = 4
    elif 200 < number <= 500:
        quality = 3
    elif 500 < number <= 1000:
        quality = 2
    else:
        quality = 1

    if not type:
        item = Item.objects.filter(quality=quality).order_by('?')[0]
    else:
        item = Item.objects.filter(type=type, quality=quality).order_by('?')[0]
    return item


def f_getRandomBook(type):
    number = random.randint(0, 2048)
    if number == 1:
        quality = 10
    elif 1 < number <= 4:
        quality = 9
    elif 4 < number <= 9:
        quality = 8
    elif 9 < number <= 19:
        quality = 7
    elif 19 < number <= 50:
        quality = 6
    elif 50 < number <= 100:
        quality = 5
    elif 100 < number <= 200:
        quality = 4
    elif 200 < number <= 500:
        quality = 3
    elif 500 < number <= 1000:
        quality = 2
    else:
        quality = 1

    if not type:
        book = Book.objects.filter(quality=quality).order_by('?')[0]
    else:
        book = Book.objects.filter(type=type, quality=quality).order_by('?')[0]
    return book


def f_getListItem(type, quality, level, order_price):
    item = None
    if type:
        item = Item.objects.filter(type=type)
    if quality:
        item = item.filter(quality=quality)
    if level:
        item = item.filter(level=level)
    if order_price == '1':
        item = item.order_by('price')
    else:
        item = item.order_by('-price')
    return item


def f_getListBook(attribute, quality, level, order_price):
    item = None
    if attribute:
        item = Book.objects.filter(attribute=attribute)
    if quality:
        item = item.filter(quality=quality)
    if level:
        item = item.filter(level=level)
    if order_price == '1':
        item = item.order_by('price')
    else:
        item = item.order_by('-price')
    return item


def f_add_properties(properties, item):
    properties_dict = dict(item.properties)
    for j in properties_dict:
        old_value = getattr(properties, j)
        setattr(properties, j, old_value + properties_dict[j])
    properties.save()


def f_remove_properties(properties, item):
    properties_dict = dict(item.properties)
    for j in properties_dict:
        old_value = getattr(properties, j)
        new_value = old_value - properties_dict[j]
        if new_value < 0: new_value = 0
        setattr(properties, j, new_value)
    properties.save()
    