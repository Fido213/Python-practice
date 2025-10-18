import pyxel
# this is an ai generated file to demonstrate a basic pyxel game structure
# i wont focus on making this a complex game, just a simple moving square
# to show understand how pyxel works
# the actual made game will be in another file

# --- 1. Global Game State Variables ---
# Define variables accessible by all functions
BALL_X = 80
BALL_Y = 60
VELOCITY_X = 1
VELOCITY_Y = 1
BALL_COLOR = 8 # Color index 8 is yellow
SCREEN_W = 160
SCREEN_H = 120


# --- 2. Update Function (Game Logic) ---
def update():
    # To modify global variables, you must declare them as 'global'
    global BALL_X, BALL_Y, VELOCITY_X, VELOCITY_Y

    # Update position
    BALL_X += VELOCITY_X
    BALL_Y += VELOCITY_Y
    # Simple boundary collision detection
    # Check left/right walls
    if BALL_X < 0 or BALL_X > SCREEN_W - 8: # 8 is the ball width
        VELOCITY_X *= -1

    # Check top/bottom walls
    if BALL_Y < 0 or BALL_Y > SCREEN_H - 8: # 8 is the ball height
        VELOCITY_Y *= -1

    # Check for quit input
    if pyxel.btnp(pyxel.KEY_ESCAPE):
        pyxel.quit()

# --- 3. Draw Function (Rendering) ---
def draw():
    # Clear the screen (cls) with black (color 0)
    pyxel.cls(0)
    
    # Draw the moving square (rect)
    # pyxel.rect(x, y, w, h, col)
    pyxel.rect(BALL_X, BALL_Y, 8, 8, BALL_COLOR)
    
    # Draw a frame count/info text
    pyxel.text(5, 5, f"Frame: {pyxel.frame_count}", 7) # Color 7 is white

# --- 4. Initialization and Run ---
# This is where the application starts
def main_game():
    # Initialize Pyxel with screen size and title
    pyxel.init(SCREEN_W, SCREEN_H, title="Procedural Pyxel Demo", fps=100)
    
    # Run the main game loop
    pyxel.run(update, draw)

# Execute the main function
main_game()