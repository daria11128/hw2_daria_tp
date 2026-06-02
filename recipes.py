class Ingredient:
    def __init__(self, name: str, quantity, unit: str):
        self.name = name
        self.unit = unit
        self.quantity = quantity  # важно: через property
    @property
    def quantity(self) -> float:
        return self._quantity
    @quantity.setter
    def quantity(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = value
    def __str__(self) -> str:
        return f"{self.name}: {self.quantity} {self.unit}"
    def __repr__(self) -> str:
        return f"Ingredient({self.name!r}, {self.quantity}, {self.unit!r})"
    def __eq__(self, other) -> bool:
        if not isinstance(other, Ingredient):
            return NotImplemented
        return self.name == other.name and self.unit == other.unit
class Recipe:
    def __init__(self, title: str, ingredients=None):
        self.title = title
        self.ingredients = list(ingredients) if ingredients is not None else []
    def add_ingredient(self, ingredient: Ingredient):
        
        for existing in self.ingredients:
            if existing == ingredient:
                existing.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)
    @staticmethod
    def is_valid_ratio(ratio) -> bool:
        return isinstance(ratio, (int, float)) and ratio > 0
    def scale(self, ratio: float):
        if not self.is_valid_ratio(ratio):
            raise ValueError("ratio must be positive")
        scaled_ingredients = [
            Ingredient(ing.name, ing.quantity * ratio, ing.unit) for ing in self.ingredients
        ]
        return Recipe(self.title, scaled_ingredients)
    def __len__(self):
        return len(self.ingredients)
    def __str__(self):
        lines = [self.title]
        for ing in self.ingredients:
            lines.append(str(ing))
        return "\n".join(lines)
class ShoppingList:
    def __init__(self):
        self._items = []
    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled = recipe.scale(portions)
        for ing in scaled.ingredients:
            self._items.append((ing, recipe.title))
    def remove_recipe(self, title: str):
        self._items = [item for item in self._items if item[1] != title]
    def get_list(self):
        totals = {}
        for ing, _recipe_title in self._items:
            key = (ing.name, ing.unit)
            totals[key] = totals.get(key, 0.0) + ing.quantity
        result = [Ingredient(name, qty, unit) for (name, unit), qty in totals.items()]
        result.sort(key=lambda x: x.name)
        return result
    def __add__(self, other):
        if not isinstance(other, ShoppingList):
            return NotImplemented
        merged = ShoppingList()
        merged._items = list(self._items) + list(other._items)
        return merged
    
class DietaryRecipe(Recipe):
    def __init__(self, title: str, diet_type: str, ingredients=None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type
    def scale(self, ratio: float):
        scaled = super().scale(ratio)
        return DietaryRecipe(scaled.title, self.diet_type, scaled.ingredients)
    def __str__(self):
        return f"[{self.diet_type}] {super().__str__()}"