import pygame
import sys

# Initialize Engines
pygame.init()
pygame.mixer.init()

# Setup Virtual Canvas (Base Design Dimensions)
BASE_WIDTH, BASE_HEIGHT = 1150, 680
canvas = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))

# Setup Scalable Display Window
WIDTH, HEIGHT = 1150, 680
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("🐼 Panda's Memory Factory Master! 🐼")
clock = pygame.time.Clock()

# --- Load Background Track ---
try:
    pygame.mixer.music.load('background_music.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
except Exception:
    pass

# --- Visual Theme Configs ---
BG_DARK = (16, 14, 23)
EDITOR_BG = (26, 24, 36)
CONVEYOR_GREY = (52, 54, 66)
LIGHT_GREY = (135, 140, 155)
TEXT_GREEN = (65, 245, 125)
TEXT_WHITE = (235, 235, 242)
BLOCK_BLUE = (0, 150, 255)
BLOCK_SHADOW = (0, 95, 190)
SLIME_GREEN = (50, 220, 90)
SLIME_SHADOW = (30, 150, 60)
WIRE_YELLOW = (245, 185, 25)
ERROR_RED = (255, 85, 85)
NARRATOR_PINK = (255, 115, 155)
ACTIVE_TAB = (50, 130, 245)
EXPLAIN_BLUE = (35, 45, 70)

# Panda Mascot Colors
PANDA_BLACK = (20, 20, 28)
PANDA_WHITE = (245, 245, 250)
PANDA_PINK = (255, 140, 175)

# --- Fonts Configuration ---
font_code = pygame.font.SysFont("menlo", 14)
font_ui = pygame.font.SysFont("arial", 15, bold=True)
font_title = pygame.font.SysFont("arial", 18, bold=True)
font_narrator = pygame.font.SysFont("arial", 14, bold=True)
font_explain = pygame.font.SysFont("arial", 14)

# --- Complete Game Architecture State ---
current_lesson = "STATIC"  # Options: "STATIC", "DYNAMIC", "2DLIST"

# Lesson Memory Data Containers
static_queue = ["DATA", "DATA", "DATA"]
static_capacity = 6

dynamic_queue = []
dynamic_capacity = 3  

matrix_grid = [
    ["EMPTY", "EMPTY", "EMPTY"],
    ["EMPTY", "BOX",   "EMPTY"],
    ["EMPTY", "EMPTY", "EMPTY"]
]

# Code Terminal Buffers
user_input_text = "static_array.append('ITEM')"
cursor_visible = True
cursor_timer = 0
terminal_feedback = "FACTORY BOOTED: Choose a lesson tab above!"
feedback_color = TEXT_GREEN
narrator_speech = "Welcome! Pick a structure to control using your Python compiler panel!"

# --- Educational Encyclopedia Data ---
lesson_explanations = {
    "STATIC": [
        "📚 WHAT IS A STATIC ARRAY?",
        "• It is a fixed row of lockers in computer memory.",
        "• The slots sit next to each other in a continuous line.",
        "• CRITICAL RULE: You cannot stretch it! If you try to",
        "  add 7 items into 6 slots, you trigger an 'Index Overflow Error'."
    ],
    "DYNAMIC": [
        "📚 WHAT IS A DYNAMIC ARRAY?",
        "• It acts like a rubber band or a stretchy slime belt!",
        "• You can append as many items as you want.",
        "• UNDER THE HOOD: When it gets completely full, Python",
        "  secretly allocates a brand new area that is DOUBLE the size!"
    ],
    "2DLIST": [
        "📚 WHAT IS A 2D LIST / MATRIX?",
        "• It is an array of arrays—viewed here from directly above!",
        "• Instead of just one index, you need coordinates: [row][col].",
        "• Think of it like a map grid where you target the precise",
        "  horizontal row and vertical column to drop your box."
    ]
}

def draw_panda_mascot(surface, center_x, center_y):
    """Renders a vector Panda Mascot on the canvas."""
    pygame.draw.circle(surface, PANDA_BLACK, (center_x - 22, center_y - 20), 10)
    pygame.draw.circle(surface, PANDA_BLACK, (center_x + 22, center_y - 20), 10)
    
    pygame.draw.ellipse(surface, PANDA_WHITE, (center_x - 30, center_y - 24, 60, 50))
    pygame.draw.ellipse(surface, PANDA_BLACK, (center_x - 30, center_y - 24, 60, 50), 2)
    
    pygame.draw.ellipse(surface, PANDA_BLACK, (center_x - 20, center_y - 8, 14, 18))
    pygame.draw.ellipse(surface, PANDA_BLACK, (center_x + 6, center_y - 8, 14, 18))
    
    pygame.draw.circle(surface, PANDA_WHITE, (center_x - 13, center_y - 2), 3)
    pygame.draw.circle(surface, PANDA_WHITE, (center_x + 13, center_y - 2), 3)
    
    pygame.draw.ellipse(surface, PANDA_BLACK, (center_x - 5, center_y + 6, 10, 6))
    
    pygame.draw.circle(surface, PANDA_PINK, (center_x - 20, center_y + 10), 5)
    pygame.draw.circle(surface, PANDA_PINK, (center_x + 20, center_y + 10), 5)

def project_3d_horizontal(x, y, z):
    """3D side view coordinate projection for linear structures."""
    fov = 280
    return int((x * fov) / z) + 810, int((y * fov) / z) + 430

def draw_3d_block(surface, x_pos, y_floor, z_depth, color_front, color_shadow, is_empty=False):
    """Draws a clean mathematical 3D factory container block."""
    w, h, d = 0.3, 0.35, 0.3
    
    p1 = project_3d_horizontal(x_pos - w, y_floor, z_depth)
    p2 = project_3d_horizontal(x_pos + w, y_floor, z_depth)
    p3 = project_3d_horizontal(x_pos + w, y_floor - h, z_depth)
    p4 = project_3d_horizontal(x_pos - w, y_floor - h, z_depth)
    
    p5 = project_3d_horizontal(x_pos - w, y_floor, z_depth + d)
    p6 = project_3d_horizontal(x_pos + w, y_floor, z_depth + d)
    p7 = project_3d_horizontal(x_pos + w, y_floor - h, z_depth + d)
    p8 = project_3d_horizontal(x_pos - w, y_floor - h, z_depth + d)
    
    if is_empty:
        pygame.draw.polygon(surface, LIGHT_GREY, [p1, p2, p6, p5], 1)
        return
        
    pygame.draw.polygon(surface, color_shadow, [p5, p6, p7, p8]) 
    pygame.draw.polygon(surface, color_shadow, [p1, p5, p8, p4]) 
    pygame.draw.polygon(surface, color_shadow, [p2, p6, p7, p3]) 
    pygame.draw.polygon(surface, color_front, [p1, p2, p3, p4])   
    pygame.draw.polygon(surface, TEXT_WHITE, [p4, p3, p7, p8]) 
    
    pygame.draw.polygon(surface, BG_DARK, [p1, p2, p3, p4], 2)
    pygame.draw.polygon(surface, BG_DARK, [p4, p3, p7, p8], 2)

# --- Core Mechanics Engine Execution Loop ---
while True:
    # 1. DRAW EVERYTHING TO VIRTUAL CANVAS
    canvas.fill(BG_DARK)
    
    # Render Layout Screen Panels Background
    pygame.draw.rect(canvas, EDITOR_BG, (0, 0, 480, 680))
    pygame.draw.line(canvas, LIGHT_GREY, (480, 0), (480, 680), 3)
    pygame.draw.rect(canvas, (22, 20, 32), (483, 0, 667, 680))
    
    # --- TOP INTERACTIVE LESSON SELECTOR TABS ---
    lessons_tabs = [("1. Static Array", "STATIC", 15), ("2. Dynamic Array", "DYNAMIC", 165), ("3. 2D Matrix Grid", "2DLIST", 320)]
    for tab_lbl, tab_id, x_offset in lessons_tabs:
        is_active = current_lesson == tab_id
        tab_col = ACTIVE_TAB if is_active else CONVEYOR_GREY
        pygame.draw.rect(canvas, tab_col, (x_offset, 15, 140, 35), border_radius=6)
        lbl_surf = font_ui.render(tab_lbl, True, TEXT_WHITE)
        canvas.blit(lbl_surf, (x_offset + 12, 23))

    # --- CODE COMPILER FRAME PANEL LAYOUT (Left Side) ---
    title_surface = font_title.render("REAL-TIME CODE WORKBENCH", True, WIRE_YELLOW)
    canvas.blit(title_surface, (25, 80))
    
    if current_lesson == "STATIC":
        inst = ["Lesson: Fixed Allocation (Contiguous Block Memory)", " > static_array.append('ITEM')", " > static_array.pop()"]
    elif current_lesson == "DYNAMIC":
        inst = ["Lesson: Dynamic Growth (Resizes automatically!)", " > dynamic_array.append('ITEM')", " > dynamic_array.pop()"]
    else:
        inst = ["Lesson: Matrices / Nested Lists [Row][Column]", " > warehouse[0][2] = 'BOX'", " > warehouse[1][1] = 'EMPTY'"]
        
    for idx, text_str in enumerate(inst):
        color = TEXT_WHITE if idx > 0 else LIGHT_GREY
        canvas.blit(font_code.render(text_str, True, color), (25, 125 + (idx * 28)))
        
    # Python Typing Input Shell box
    pygame.draw.rect(canvas, BG_DARK, (25, 235, 430, 45), border_radius=6)
    pygame.draw.rect(canvas, WIRE_YELLOW, (25, 235, 430, 45), 2, border_radius=6)
    
    cursor_timer += 1
    if cursor_timer % 30 == 0:
        cursor_visible = not cursor_visible
        
    render_input = user_input_text + ("|" if cursor_visible else "")
    canvas.blit(font_code.render(render_input, True, TEXT_WHITE), (35, 248))
    
    # Terminal Display Box Output logs
    pygame.draw.rect(canvas, BG_DARK, (25, 315, 430, 140), border_radius=6)
    canvas.blit(font_ui.render("CONSOLE ARCHITECTURE LOGS:", True, LIGHT_GREY), (25, 290))
    canvas.blit(font_code.render(terminal_feedback, True, feedback_color), (35, 335))
    
    # --- 📚 THE DYNAMIC VISUAL EXPLAINER PANEL (Bottom Left) ---
    pygame.draw.rect(canvas, EXPLAIN_BLUE, (25, 490, 430, 160), border_radius=8)
    lines = lesson_explanations[current_lesson]
    for idx, line in enumerate(lines):
        text_color = WIRE_YELLOW if idx == 0 else TEXT_WHITE
        canvas.blit(font_explain.render(line, True, text_color), (40, 505 + (idx * 26)))
    
    # --- 🐼 PANDA MASCOT & SPEECH BUBBLE (Right Side Top) ---
    draw_panda_mascot(canvas, 545, 112)
    
    # Draw Speech Box Pointer & Bubble
    pygame.draw.polygon(canvas, NARRATOR_PINK, [(585, 110), (598, 102), (598, 118)])
    pygame.draw.rect(canvas, NARRATOR_PINK, (595, 80, 525, 65), border_radius=12)
    canvas.blit(font_narrator.render(narrator_speech, True, BG_DARK), (610, 102))

    # --- DYNAMIC VIEWPORTS PANEL ---
    if current_lesson == "STATIC":
        r1, r2 = project_3d_horizontal(-2.2, 0.4, 2.5), project_3d_horizontal(2.2, 0.4, 2.5)
        r3, r4 = project_3d_horizontal(2.2, 0.4, 2.9), project_3d_horizontal(-2.2, 0.4, 2.9)
        pygame.draw.polygon(canvas, CONVEYOR_GREY, [r1, r2, r3, r4])
        pygame.draw.line(canvas, WIRE_YELLOW, r1, r2, 4)
        
        for slot in range(static_capacity):
            x_step = -1.6 + (slot * 0.62)
            draw_3d_block(canvas, x_step, 0.4, 2.5, BLOCK_BLUE, BLOCK_SHADOW, is_empty=(slot >= len(static_queue)))
        canvas.blit(font_ui.render(f"STATIC ARRAY CELLS UTILIZED: {len(static_queue)} / {static_capacity}", True, TEXT_WHITE), (510, 25))

    elif current_lesson == "DYNAMIC":
        r1, r2 = project_3d_horizontal(-2.2, 0.4, 2.5), project_3d_horizontal(2.2, 0.4, 2.5)
        pygame.draw.line(canvas, SLIME_GREEN, r1, r2, 6)
        
        for slot in range(dynamic_capacity):
            x_step = -1.7 + (slot * (3.4 / dynamic_capacity))
            draw_3d_block(canvas, x_step, 0.4, 2.5, SLIME_GREEN, SLIME_SHADOW, is_empty=(slot >= len(dynamic_queue)))
            
        canvas.blit(font_ui.render(f"DYNAMIC ARRAY ALLOCATION SIZE: {len(dynamic_queue)} / {dynamic_capacity}", True, TEXT_WHITE), (510, 25))

    elif current_lesson == "2DLIST":
        canvas.blit(font_ui.render("FACTORY Warehouse Map (2D Grid Top-View Map Mode)", True, TEXT_WHITE), (510, 25))
        
        start_x, start_y = 590, 220
        cell_size, gap = 110, 15
        
        for r_idx in range(3):
            for c_idx in range(3):
                cell_x = start_x + (c_idx * (cell_size + gap))
                cell_y = start_y + (r_idx * (cell_size + gap))
                
                is_box = matrix_grid[r_idx][c_idx] == "BOX"
                
                if is_box:
                    pygame.draw.rect(canvas, BLOCK_BLUE, (cell_x, cell_y, cell_size, cell_size), border_radius=10)
                    pygame.draw.rect(canvas, BLOCK_SHADOW, (cell_x + 6, cell_y + 6, cell_size - 12, cell_size - 12), border_radius=6)
                    txt_col = TEXT_WHITE
                else:
                    pygame.draw.rect(canvas, CONVEYOR_GREY, (cell_x, cell_y, cell_size, cell_size), border_radius=10, width=2)
                    txt_col = LIGHT_GREY
                
                addr_str = f"[{r_idx}][{c_idx}]"
                val_str = matrix_grid[r_idx][c_idx]
                
                canvas.blit(font_code.render(addr_str, True, txt_col), (cell_x + 12, cell_y + 15))
                canvas.blit(font_ui.render(val_str, True, WIRE_YELLOW if is_box else LIGHT_GREY), (cell_x + 12, cell_y + 60))

    # 2. SCALE CANVAS TO DISPLAY WINDOW (Maintaining Aspect Ratio or Fitting Screen)
    win_w, win_h = screen.get_size()
    scaled_canvas = pygame.transform.smoothscale(canvas, (win_w, win_h))
    screen.blit(scaled_canvas, (0, 0))

    # --- Interactive Controls Input Capture Processing Loops ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Map window mouse position back to virtual canvas coordinates
            raw_mx, raw_my = event.pos
            mx = int(raw_mx * (BASE_WIDTH / win_w))
            my = int(raw_my * (BASE_HEIGHT / win_h))

            # Tab clicks triggers
            if 15 <= my <= 50:
                if 15 <= mx <= 155:
                    current_lesson = "STATIC"
                    user_input_text = "static_array.append('ITEM')"
                    terminal_feedback = "LOADED: Fixed size array testing ground."
                    narrator_speech = "Look down at the blue board to learn about Fixed memory allocation!"
                elif 165 <= mx <= 305:
                    current_lesson = "DYNAMIC"
                    user_input_text = "dynamic_array.append('ITEM')"
                    terminal_feedback = "LOADED: Dynamic Resizable array vector ground."
                    narrator_speech = "Try appending past the 3 boxes to see the array automatically grow!"
                elif 320 <= mx <= 460:
                    current_lesson = "2DLIST"
                    user_input_text = "warehouse[0][2] = 'BOX'"
                    terminal_feedback = "LOADED: 2D Multi-dimensional index plane."
                    narrator_speech = "Look! We can now inspect the 2D List directly from a Top-Down view grid map!"
                    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_input_text = user_input_text[:-1]
            elif event.key == pygame.K_RETURN:
                cmd = user_input_text.strip().replace(" ", "")
                
                if current_lesson == "STATIC":
                    if cmd == "static_array.append('ITEM')":
                        if len(static_queue) < static_capacity:
                            static_queue.append("DATA")
                            terminal_feedback = "SUCCESS: Pushed variable straight down into sequential memory block!"
                            narrator_speech = "Super-duper! The fixed memory cells accepted our input perfectly!"
                            feedback_color = TEXT_GREEN
                        else:
                            terminal_feedback = "FATAL EXCEPTION: IndexError! Static array out of bounds!"
                            narrator_speech = "Uh-oh! A Fixed array cannot expand past its initial pre-allocated size!"
                            feedback_color = ERROR_RED
                    elif cmd == "static_array.pop()":
                        if len(static_queue) > 0:
                            static_queue.pop()
                            terminal_feedback = "SUCCESS: Deallocated the right-most slot index storage cell space."
                            narrator_speech = "Zoom! Element removed cleanly out from the memory map sequence stack!"
                            feedback_color = TEXT_GREEN
                        else:
                            terminal_feedback = "Underflow Error: Array structure is already clean!"
                            feedback_color = ERROR_RED
                            
                elif current_lesson == "DYNAMIC":
                    if cmd == "dynamic_array.append('ITEM')":
                        dynamic_queue.append("DATA")
                        terminal_feedback = "SUCCESS: Element inserted into Dynamic vector array structures."
                        narrator_speech = "Neat! Python managed allocation behind the scenes."
                        feedback_color = TEXT_GREEN
                        
                        if len(dynamic_queue) > dynamic_capacity:
                            old_cap = dynamic_capacity
                            dynamic_capacity *= 2
                            terminal_feedback = f"CAPACITY RESIZE: Array grew from {old_cap} cells to {dynamic_capacity}!"
                            narrator_speech = "Wow! Dynamic Arrays automatically DOUBLE memory capacity when full!"
                            feedback_color = WIRE_YELLOW
                    elif cmd == "dynamic_array.pop()":
                        if len(dynamic_queue) > 0:
                            dynamic_queue.pop()
                            terminal_feedback = "SUCCESS: Popped last allocated list object element container."
                            feedback_color = TEXT_GREEN
                            
                elif current_lesson == "2DLIST":
                    try:
                        if "warehouse[" in cmd and "]=" in cmd:
                            coords, val = cmd.split("]=")
                            r_c = coords.replace("warehouse[", "").split("][")
                            r, c = int(r_c[0]), int(r_c[1])
                            val_str = val.replace("'", "").replace('"', "")
                            
                            if val_str in ["BOX", "EMPTY"] and 0 <= r < 3 and 0 <= c < 3:
                                matrix_grid[r][c] = val_str
                                terminal_feedback = f"SUCCESS: Overwrote matrix node cell target at row {r}, col {c}."
                                narrator_speech = "Whiz-bang! You targeted a precise cross-intersection coordinate cell!"
                                feedback_color = TEXT_GREEN
                            else:
                                raise ValueError()
                        else:
                            raise ValueError()
                    except Exception:
                        terminal_feedback = "SyntaxError: Must match format warehouse[row][col] = 'BOX' (0-2 max)"
                        feedback_color = ERROR_RED
            else:
                if len(user_input_text) < 42:
                    user_input_text += event.unicode

    pygame.display.flip()
    clock.tick(60)