
def startScreen():
    entry_font = pygame.font.Font(cst.font, 75)
    entries = ['Start', 'Quit']
    selected_entry = 0

    while True:
        display.fill(color.background)

        for event in pygame.event.get():  # Managing Inputs
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_UP or event.key == K_w:
                    selected_entry = (selected_entry - 1) % len(entries)
                elif event.key == K_DOWN or event.key == K_s:
                    selected_entry = (selected_entry + 1) % len(entries)
                elif event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_RETURN:
                    if selected_entry == 0:
                        RunGame()
                    elif selected_entry == 1:
                        terminate()

        drawTitle()
        # Drawing Menu Entries
        for i in range(len(entries)):
            if i == selected_entry:
                entry_color = color.hover
            else:
                entry_color = color.foreground

            entry_obj = entry_font.render(entries[i], 1, entry_color)
            entry_rect = entry_obj.get_rect()
            entry_rect.center = (widthOfWindow / 2, 250 + 110 * i)
            display.blit(entry_obj, entry_rect)

        pygame.display.update()
        fps.tick(FPS)