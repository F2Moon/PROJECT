import pygame
import pygame_gui
import random
#import time

# --- เริ่มต้นการใช้งาน Pygame และตั้งค่าหน้าจอ --- #
pygame.init()
pygame.display.set_caption('Circle Click Game')  # ชื่อหน้าต่างเกม
WIDTH, HEIGHT = 800, 600  # ขนาดหน้าจอ
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((WIDTH, HEIGHT))  # ตัวจัดการ UI (จาก pygame_gui)

# --- ตัวแปรสถานะของเกม --- #
STATE_MENU = 'menu'        # หน้าเมนู
STATE_SETTINGS = 'settings' # หน้าตั้งค่า
STATE_GAME = 'game'        # หน้าเล่นเกม
STATE_END = 'end'          # หน้าจบเกม
state = STATE_MENU         # เริ่มต้นที่หน้าเมนู

# --- ตัวแปรตั้งค่าพื้นฐานของเกม --- #
circle_radius = 30           # รัศมีวงกลมเริ่มต้น
circle_duration = 2000       # เวลาที่วงกลมแสดงต่อครั้ง (ms)
game_time_limit = 30000      # เวลาจำกัดการเล่นทั้งหมด (30 วินาที)

# --- ตัวแปรข้อมูลผู้เล่น --- #
player_name = ""
score = 0
game_start_time = 0

# --- สร้าง UI ของหน้า MENU --- #
welcome_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((250, 80), (300, 100)), text="Welcome to Click Game", manager=manager)
name_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((300, 150), (200, 30)), manager=manager)
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((325, 200), (150, 40)), text="Start", manager=manager)
settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((325, 250), (150, 40)), text="Settings", manager=manager)
exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((325, 300), (150, 40)), text="Exit", manager=manager)

# ฟังก์ชันสำหรับแสดง/ซ่อน UI ของหน้า MENU
def toggle_menu_ui(visible):
    if visible:
        welcome_label.show()
        name_input.show()
        start_button.show()
        settings_button.show()
        exit_button.show()
    else:
        welcome_label.hide()
        name_input.hide()
        start_button.hide()
        settings_button.hide()
        exit_button.hide()

# --- สร้าง UI ของหน้า SETTINGS --- #
radius_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((150, 150), (200, 30)), text="Radius", manager=manager)
radius_slider = pygame_gui.elements.UIHorizontalSlider(pygame.Rect((300, 150), (200, 30)), circle_radius, (10, 100), manager=manager)
radius_value_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((520, 150), (60, 30)), text=str(circle_radius), manager=manager)

duration_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((150, 200), (200, 30)), text="Duration (ms)", manager=manager)
duration_slider = pygame_gui.elements.UIHorizontalSlider(pygame.Rect((300, 200), (200, 30)), circle_duration, (500, 5000), manager=manager)
duration_value_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((520, 200), (60, 30)), text=str(circle_duration), manager=manager)

time_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((150, 250), (200, 30)), text="Time Limit (s)", manager=manager)
time_slider = pygame_gui.elements.UIHorizontalSlider(pygame.Rect((300, 250), (200, 30)), game_time_limit // 1000, (5, 120), manager=manager)
time_value_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((520, 250), (60, 30)), text=str(game_time_limit), manager=manager)

back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((325, 320), (150, 40)), text="Back", manager=manager)

# ฟังก์ชันสำหรับแสดง/ซ่อน UI ของหน้า SETTINGS
def toggle_settings_ui(visible):
    if visible:
        radius_label.show()
        duration_label.show()
        time_label.show()
        radius_slider.show()
        duration_slider.show()
        time_slider.show()
        radius_value_label.show()
        duration_value_label.show()
        time_value_label.show()
        back_button.show()
    else:
        radius_label.hide()
        duration_label.hide()
        time_label.hide()
        radius_slider.hide()
        duration_slider.hide()
        time_slider.hide()
        radius_value_label.hide()
        duration_value_label.hide()
        time_value_label.hide()
        back_button.hide()

toggle_settings_ui(False)  # ตอนเริ่มต้นซ่อนหน้า settings ไว้ก่อน

# --- ตัวแปรในระหว่างเล่นเกม --- #
circle_pos = (0, 0)  # ตำแหน่งวงกลม
next_time = 0        # เวลาสำหรับแสดงวงกลมถัดไป
SAFE_TOP_MARGIN = 60  # ระยะด้านบนที่ไม่ให้มีวงกลม (px)

# ฟังก์ชันเริ่มเกมใหม่
def reset_game():
    global score, circle_pos, next_time, game_start_time
    score = 0
    circle_pos = (random.randint(circle_radius, WIDTH - circle_radius), random.randint(circle_radius + SAFE_TOP_MARGIN, HEIGHT - circle_radius))
    next_time = pygame.time.get_ticks() + circle_duration
    game_start_time = pygame.time.get_ticks()  # บันทึกเวลาที่เริ่มเล่น

# --- วนลูปหลักของเกม --- #
running = True
while running:
    time_delta = clock.tick(60) / 1000  # ควบคุม FPS 60 เฟรมต่อวินาที
    screen.fill((0, 0, 0))  # เคลียร์หน้าจอเป็นสีดำทุกเฟรม

    if state == STATE_GAME:
        now = pygame.time.get_ticks()

        # เช็คหมดเวลาไหม
        if now - game_start_time >= game_time_limit:
            state = STATE_END
            continue

        # วาดวงกลมใหม่ถ้าหมดเวลาแสดง
        if now >= next_time:
            while True:
                new_x = random.randint(circle_radius, WIDTH - circle_radius)
                new_y = random.randint(circle_radius + SAFE_TOP_MARGIN, HEIGHT - circle_radius)
        
                # เช็คว่าอยู่ในบริเวณปลอดภัย
                if new_y > SAFE_TOP_MARGIN:
                    circle_pos = (new_x, new_y)
                    break

            next_time = now + circle_duration

        # วาดวงกลม
        pygame.draw.circle(screen, (255, 0, 0), circle_pos, circle_radius)

        # แสดงคะแนน
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"{player_name} | Score: {score}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        # แสดงเวลาที่เหลือแบบเท่ๆ
        time_left = max(0, (game_time_limit - (now - game_start_time)) // 1000)
        if time_left <= 5:
            color = (255, 0, 0)  # แดงถ้าเหลือ <=5 วิ
        else:
            color = (255, 255, 0)  # เหลืองปกติ
        time_font = pygame.font.SysFont(None, 36)
        time_text = time_font.render(f"Time Left: {time_left}s", True, color)
        time_rect = time_text.get_rect(topright=(WIDTH - 10, 10))  # ชิดขวา 10px, ชิดบน 10px
        screen.blit(time_text, time_rect)

    # หน้า SETTINGS: อัพเดตค่าต่างๆ
    if state == STATE_SETTINGS:
        current_radius = int(radius_slider.get_current_value())
        current_duration = int(duration_slider.get_current_value())
        current_time = int(time_slider.get_current_value())

        radius_value_label.set_text(str(current_radius))
        duration_value_label.set_text(str(current_duration))
        time_value_label.set_text(str(current_time))
        pygame.draw.circle(screen, (255, 0, 0), (WIDTH//2, 480), current_radius)

    # หน้า END: แสดงผลคะแนนหลังเล่นจบ
    if state == STATE_END:
        font = pygame.font.SysFont(None, 50)
        text_surface = font.render(f"{player_name} | Score: {score}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 250))
        screen.blit(text_surface, text_rect)
        back_button.show()

    # อัพเดต UI และวาดบนหน้าจอ
    manager.update(time_delta)
    manager.draw_ui(screen)
    pygame.display.update()

    # --- จัดการเหตุการณ์ต่างๆ --- #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if state != STATE_GAME:
            manager.process_events(event)

        if state == STATE_GAME and event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            dx, dy = mx - circle_pos[0], my - circle_pos[1]
            if (dx**2 + dy**2) ** 0.5 <= circle_radius:
                score += 1
                next_time = 0  # คลิกโดน สร้างจุดใหม่ทันที

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == start_button:
                player_name = name_input.get_text()
                reset_game()
                toggle_menu_ui(False)
                toggle_settings_ui(False)
                state = STATE_GAME

            elif event.ui_element == settings_button:
                toggle_settings_ui(True)
                toggle_menu_ui(False)
                state = STATE_SETTINGS

            elif event.ui_element == back_button:
                # บันทึกค่าที่ปรับไว้
                circle_radius = int(radius_slider.get_current_value())
                circle_duration = int(duration_slider.get_current_value())
                game_time_limit = int(time_slider.get_current_value()) * 1000
                toggle_menu_ui(True)
                toggle_settings_ui(False)
                state = STATE_MENU

            elif event.ui_element == exit_button:
                running = False
                pygame.quit()
