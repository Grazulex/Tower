# Game starting values
STARTING_POINTS = 300
STARTING_LIVES = 20

# Window and Display Settings
TITLE = 'Tower Defense'  # Title of the game window
CELL_SIZE = 20  # Size of each grid cell in pixels

# Board Dimensions
BOARD_WIDTH = 800  # Width of the game board in pixels
BOARD_HEIGHT = 400  # Height of the game board in pixels
UI_WIDTH = 150  # Width of the user interface area in pixels
WINDOW_WIDTH = BOARD_WIDTH + UI_WIDTH  # Total width of the game window
WINDOW_HEIGHT = BOARD_HEIGHT  # Total height of the game window

# Game Track Settings
TRACK_WIDTH = 2  # Width of the enemy path in grid cells

# Tower Properties
TOUR_RANGE = 50  # Default attack range of towers in pixels
ATTACK_DURATION = 500  # Duration of tower attacks in milliseconds

# Normal Tower Properties
NORMAL_TOWER_RANGE = 50  # Attack range of normal towers in pixels
NORMAL_TOWER_ATTACK_SPEED = 1.0  # Attack speed of normal towers (attacks per second)
NORMAL_TOWER_DAMAGE = 25  # Damage dealt by normal towers per attack
NORMAL_TOWER_COST = 100  # Cost of normal towers in game points

# Slow Tower Properties
SLOW_TOWER_RANGE = 90  # Attack range of slow towers in pixels
SLOW_TOWER_ATTACK_SPEED = 0.5  # Attack speed of slow towers (attacks per second)
SLOW_TOWER_DAMAGE = 75  # Damage dealt by slow towers per attack
SLOW_TOWER_COST = 175  # Cost of slow towers in game points

# Power Tower Properties
POWER_TOWER_RANGE = 45  # Attack range of power towers in pixels
POWER_TOWER_ATTACK_SPEED = 2.0  # Attack speed of power towers (attacks per second)
POWER_TOWER_DAMAGE = 15  # Damage dealt by power towers per attack
POWER_TOWER_COST = 150  # Cost of power towers in game points

# Enemy Properties
ENEMY_RADIUS = 10  # Base size of enemy units in pixels
ENEMY_SPEED = 2  # Base movement speed of enemies in pixels per frame

# Normal Enemy Properties
NORMAL_ENEMY_HEALTH = 150  # Health points of normal enemies
NORMAL_ENEMY_POINTS = 25  # Points awarded for defeating normal enemies

# Small Enemy Properties
SMALL_ENEMY_RADIUS_MULTIPLIER = 0.8  # Size multiplier for small enemies
SMALL_ENEMY_HEALTH = 75  # Health points of small enemies
SMALL_ENEMY_SPEED_MULTIPLIER = 2.5  # Speed multiplier for small enemies
SMALL_ENEMY_POINTS = 35  # Points awarded for defeating small enemies

# Big Enemy Properties
BIG_ENEMY_RADIUS_MULTIPLIER = 1.2  # Size multiplier for big enemies
BIG_ENEMY_HEALTH = 300  # Health points of big enemies
BIG_ENEMY_SPEED_MULTIPLIER = 0.4  # Speed multiplier for big enemies
BIG_ENEMY_POINTS = 50  # Points awarded for defeating big enemies

# Visual Effects Settings
# Tower range visualization
RANGE_CIRCLES_COUNT = 3  # Number of concentric circles for range display
RANGE_MAX_ALPHA = 40  # Maximum transparency for range circles (0-255)
RANGE_MIN_ALPHA = 15  # Minimum transparency for range circles (0-255)
RANGE_COLOR_INTENSITY = 30  # How much to lighten the tower's color for range display
RANGE_GLOW_ALPHA = 15  # Transparency for the glow effect

# Tower gradient effect
TOWER_GRADIENT_INTENSITY = 40  # How much to darken the tower's color for gradient

# Enemy health visualization
ENEMY_DAMAGED_COLOR = (255, 100, 100)  # Color for damaged enemies
ENEMY_HEALTH_GRADIENT_STEPS = 10  # Number of steps in the health gradient

# Particle effects
PARTICLE_COLOR_VARIATION = 20  # Maximum color variation for particles
PARTICLE_SIZE_MIN = 2  # Minimum particle size
PARTICLE_SIZE_MAX = 4  # Maximum particle size
PARTICLE_LIFETIME_MIN = 25  # Minimum particle lifetime
PARTICLE_LIFETIME_MAX = 35  # Maximum particle lifetime
PARTICLE_SPEED = 1.5  # Base particle movement speed
