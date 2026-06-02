import pytest
from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe
def test_ingredient_init():
    ing = Ingredient("Мука", 500, "г")
    assert ing.name == "Мука"
    assert ing.unit == "г"
    assert ing.quantity == 500.0
def test_ingredient_str():
    ing = Ingredient("Мука", 500, "г")
    assert str(ing) == "Мука: 500.0 г"
def test_ingredient_eq_ignores_quantity():
    a = Ingredient("Мука", 100, "г")
    b = Ingredient("Мука", 999, "г")
    assert a == b
def test_ingredient_not_equal_by_name_or_unit():
    assert Ingredient("Мука", 1, "г") != Ingredient("Сахар", 1, "г")
    assert Ingredient("Мука", 1, "г") != Ingredient("Мука", 1, "кг")
def test_ingredient_quantity_must_be_positive():
    with pytest.raises(ValueError, match="Количество должно быть положительным"):
        Ingredient("Мука", 0, "г")

def test_recipe_add_ingredient_sums_quantity():
    r = Recipe("Пирог", [])
    r.add_ingredient(Ingredient("Мука", 100, "г"))
    r.add_ingredient(Ingredient("Мука", 50, "г"))
    assert len(r) == 1
    assert r.ingredients[0].quantity == 150.0
def test_recipe_scale_returns_new_and_does_not_change_original():
    r = Recipe("Пирог", [Ingredient("Мука", 100, "г"), Ingredient("Яйца", 2, "шт")])
    r2 = r.scale(3)
    assert r2 is not r
    assert r2.title == r.title
    assert r.ingredients[0].quantity == 100.0
    assert r.ingredients[1].quantity == 2.0
    assert r2.ingredients[0].quantity == 300.0
    assert r2.ingredients[1].quantity == 6.0
def test_recipe_scale_raises_on_non_positive_ratio():
    r = Recipe("Пирог", [Ingredient("Мука", 100, "г")])
    with pytest.raises(ValueError):
        r.scale(0)
    with pytest.raises(ValueError):
        r.scale(-1)

def test_shopping_list_add_recipe_and_portions_validation():
    r = Recipe("Пирог", [Ingredient("Мука", 100, "г")])
    s = ShoppingList()
    with pytest.raises(ValueError, match="Количество порций должно быть положительным"):
        s.add_recipe(r, 0)
    s.add_recipe(r, 2)
    out = s.get_list()
    assert len(out) == 1
    assert out[0].name == "Мука"
    assert out[0].unit == "г"
    assert out[0].quantity == 200.0
def test_shopping_list_remove_recipe():
    r1 = Recipe("A", [Ingredient("Мука", 100, "г")])
    r2 = Recipe("B", [Ingredient("Сахар", 50, "г")])
    s = ShoppingList()
    s.add_recipe(r1, 1)
    s.add_recipe(r2, 1)
    s.remove_recipe("A")
    out = s.get_list()
    assert len(out) == 1
    assert out[0].name == "Сахар"
    s.remove_recipe("NOPE")
def test_shopping_list_get_list_sums_and_sorts():
    r1 = Recipe("A", [Ingredient("Мука", 100, "г"), Ingredient("Сахар", 10, "г")])
    r2 = Recipe("B", [Ingredient("Мука", 50, "г")])
    s = ShoppingList()
    s.add_recipe(r1, 1)
    s.add_recipe(r2, 2)  # мука +100
    out = s.get_list()
    assert [i.name for i in out] == sorted([i.name for i in out])
    flour = [i for i in out if i.name == "Мука"][0]
    assert flour.quantity == 200.0
def test_shopping_list_add_operator_creates_new():
    r = Recipe("A", [Ingredient("Мука", 100, "г")])
    s1 = ShoppingList()
    s1.add_recipe(r, 1)
    s2 = ShoppingList()
    s2.add_recipe(r, 2)
    s3 = s1 + s2
    assert s3 is not s1 and s3 is not s2
    assert len(s1.get_list()) == 1
    assert len(s2.get_list()) == 1
    assert len(s3.get_list()) == 1
    assert s3.get_list()[0].quantity == 300.0
    
def test_dietary_recipe_str_and_scale_type():
    r = DietaryRecipe("Пицца", "веган", [Ingredient("Тесто", 300, "г")])
    assert str(r).startswith("[веган]")
    r2 = r.scale(2)
    assert isinstance(r2, DietaryRecipe)
    assert r2.diet_type == "веган"
    assert r2.ingredients[0].quantity == 600.0
