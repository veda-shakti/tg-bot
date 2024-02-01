from swisseph import set_ephe_path, set_sid_mode, SIDM_LAHIRI

def setup_utils():
    set_ephe_path('assets/ephe')
    set_sid_mode(SIDM_LAHIRI)