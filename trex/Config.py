class Config:
    START_PAUSE = 0
    AUTO_ALT_TAB = True
    KEY_QUIT_OPENCV = 'q'

    start_padding = [150, 300, 300, 300]

    trex_color_limits = (123, 128)

    # начальное соотношение ближайшего x объектов к ширине игровой области
    default_ratio_for_jump = 0.07
    # начальная задержка до увеличения ratio_for_jump
    default_delay_for_increase_ratio = 6
    # множитель ratio_for_jump
    factor_ratio_for_jump = 1.15
    # множитель delay_for_increase_ratio
    factor_delay_for_increase_ratio = 0.98
