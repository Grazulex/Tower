# Window and Display Settings
TITLE = 'Tower Defense'
CELL_SIZE = 20  # Size of each grid cell in pixels

# Board Dimensions
BOARD_WIDTH = 800
BOARD_HEIGHT = 400
UI_WIDTH = 150
WINDOW_WIDTH = BOARD_WIDTH + UI_WIDTH
WINDOW_HEIGHT = BOARD_HEIGHT

# Game Track Settings
TRACK_WIDTH = 2  # Width of the enemy path

# Tower Properties
TOUR_RANGE = 50        # Default attack range of towers
ATTACK_DURATION = 500  # Duration of tower attacks in milliseconds

# Normal Tower Properties
NORMAL_TOWER_RANGE = 50
NORMAL_TOWER_ATTACK_SPEED = 1.0
NORMAL_TOWER_DAMAGE = 25
NORMAL_TOWER_COST = 100

# Slow Tower Properties
SLOW_TOWER_RANGE = 90
SLOW_TOWER_ATTACK_SPEED = 0.5
SLOW_TOWER_DAMAGE = 75
SLOW_TOWER_COST = 175

# Power Tower Properties
POWER_TOWER_RANGE = 45
POWER_TOWER_ATTACK_SPEED = 2.0
POWER_TOWER_DAMAGE = 15
POWER_TOWER_COST = 150

# Enemy Properties
ENEMY_RADIUS = 10      # Base size of enemy units
ENEMY_SPEED = 2        # Base movement speed of enemies

# Normal Enemy Properties
NORMAL_ENEMY_HEALTH = 150
NORMAL_ENEMY_POINTS = 25

# Small Enemy Properties
SMALL_ENEMY_RADIUS_MULTIPLIER = 0.8
SMALL_ENEMY_HEALTH = 75
SMALL_ENEMY_SPEED_MULTIPLIER = 2.5
SMALL_ENEMY_POINTS = 35

# Big Enemy Properties
BIG_ENEMY_RADIUS_MULTIPLIER = 1.2
BIG_ENEMY_HEALTH = 300
BIG_ENEMY_SPEED_MULTIPLIER = 0.4
BIG_ENEMY_POINTS = 50
