class Config:
    START_PAUSE = 0
    KEY_QUIT_OPENCV = 'q'

    start_padding = 100
    default_game_area_width = 521
    default_game_area_height = 119

    trex_color_limits = 83

    # начальное соотношение ближайшего x объектов к ширине игровой области
    default_ratio_for_jump = 0.07
    # начальная задержка до увеличения ratio_for_jump
    default_delay_for_increase_ratio = 6
    # множитель ratio_for_jump
    factor_ratio_for_jump = 1.15
    # множитель delay_for_increase_ratio
    factor_delay_for_increase_ratio = 0.98
