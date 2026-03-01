from copy import deepcopy

__all__ = ("get_catalog_items", "get_item_by_pk")

_STATIC_ITEMS = [
    {
        "pk": 1,
        "name": "Кофе в зёрнах",
        "text": "Роскошно насыщенный вкус с шоколадным послевкусием.",
        "image_url": "img/coffee.jpg",
        "image_alt": "Упаковка кофе в зёрнах",
    },
    {
        "pk": 2,
        "name": "Чай улун",
        "text": "Превосходно ароматный чай для спокойного вечера.",
        "image_url": "img/tea.jpg",
        "image_alt": "Чай улун в стеклянной банке",
    },
    {
        "pk": 3,
        "name": "Печенье с миндалём",
        "text": "Превосходно хрустящее печенье к чаю и кофе.",
        "image_url": "img/cookies.jpg",
        "image_alt": "Печенье с миндалём на тарелке",
    },
    {
        "pk": 4,
        "name": "Сироп карамельный",
        "text": "Роскошно дополняет десерты, кофе и молочные коктейли.",
        "image_url": "img/sirop.jpg",
        "image_alt": "Бутылка карамельного сиропа",
    },
]


def get_catalog_items():
    return deepcopy(_STATIC_ITEMS)


def get_item_by_pk(pk):
    for item in _STATIC_ITEMS:
        if item["pk"] == pk:
            return deepcopy(item)

    fallback = deepcopy(_STATIC_ITEMS[0])
    fallback["pk"] = pk
    return fallback
