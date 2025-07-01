# Dungeon/levelGenerator.py
def generate_level(width=100, height=100):
    # Example: fill with dots, you can customize this
    return tuple("." * width for _ in range(height))