SKU_DICT = {
    # --- Example Entries ---    
    'SP_194M_M': {'design': '194M', 'color': 'GREEN', 'size': 'M'},
    'SP_194M_L': {'design': '194M', 'color': 'GREEN', 'size': 'L'},
    'SP_194M_XL': {'design': '194M', 'color': 'GREEN', 'size': 'XL'},
    '194M_36':   {'design': '194M', 'color': 'GREEN', 'size': 'M'},
    '194M_38':   {'design': '194M', 'color': 'GREEN', 'size': 'L'},
    '194M_40':   {'design': '194M', 'color': 'GREEN', 'size': 'XL'},
    '188M_WHITE_M': {'design': '188M', 'color': 'WHITE', 'size': 'M'},
    '188M_WHITE_36': {'design': '188M', 'color': 'WHITE', 'size': 'M'},
    '188M_WHITE_38': {'design': '188M', 'color': 'WHITE', 'size': 'L'},
    '188M_WHITE_L': {'design': '188M', 'color': 'WHITE', 'size': 'L'},
    '188M_WHITE_XL': {'design': '188M', 'color': 'WHITE', 'size': 'XL'},
    '188M_WHITE_40': {'design': '188M', 'color': 'WHITE', 'size': 'XL'},
    '188M_PINK_M': {'design': '188M', 'color': 'PINK', 'size': 'M'},
    '188M_PINK_L': {'design': '188M', 'color': 'PINK', 'size': 'L'},
    '188M_PINK_XL': {'design': '188M', 'color': 'PINK', 'size': 'XL'},
    '205M_PINK_M': {'design': '205M', 'color': 'PINK', 'size': 'M'},
    'SP_205M_PINK_M': {'design': '205M', 'color': 'PINK', 'size': 'M'},
    '205M_PINK_L': {'design': '205M', 'color': 'PINK', 'size': 'L'},
    'SP_205M_PINK_L': {'design': '205M', 'color': 'PINK', 'size': 'L'},
    '205M_PINK_XL': {'design': '205M', 'color': 'PINK', 'size': 'XL'},
    'SP_205M_PINK_XL': {'design': '205M', 'color': 'PINK', 'size': 'XL'},
    '205M_GREEN_M': {'design': '205M', 'color': 'GREEN', 'size': 'M'},
    'SP_205M_GREEN_M': {'design': '205M', 'color': 'GREEN', 'size': 'M'},
    '205M_GREEN_L': {'design': '205M', 'color': 'GREEN', 'size': 'L'},
    'SP_205M_GREEN_L': {'design': '205M', 'color': 'GREEN', 'size': 'L'},
    '205M_GREEN_XL': {'design': '205M', 'color': 'GREEN', 'size': 'XL'},
    'SP_205M_GREEN_XL': {'design': '205M', 'color': 'GREEN', 'size': 'XL'},
    '003.13WFM_OFFW_S': {'design': '003W', 'color': 'OFFW', 'size': 'S'},
    '003.13WFM_OFFW_M': {'design': '003W', 'color': 'OFFW', 'size': 'M'},
    '003.13WFM_OFFW_L': {'design': '003W', 'color': 'OFFW', 'size': 'L'},
    '003.13WFM_OFFW_XL': {'design': '003W', 'color': 'OFFW', 'size': 'XL'},
    'SP_188M_WHITE_36': {'design': '188M', 'color': 'WHITE', 'size': 'M'},
    'SP_188M_WHITE_38': {'design': '188M', 'color': 'WHITE', 'size': 'L'},
    'SP_188M_WHITE_40': {'design': '188M', 'color': 'WHITE', 'size': 'XL'},
    'SP_188M_40': {'design': '188M', 'color': 'WHITE', 'size': 'XL'},
    'SP_188M_38': {'design': '188M', 'color': 'WHITE', 'size': 'L'},
    'SP_188M_36': {'design': '188M', 'color': 'WHITE', 'size': 'M'},
    '003.13WFM_PLUM_S': {'design': '003W', 'color': 'PLUM', 'size': 'S'},
    '003.13WFM_PLUM_M': {'design': '003W', 'color': 'PLUM', 'size': 'M'},
    '003.13WFM_PLUM_L': {'design': '003W', 'color': 'PLUM', 'size': 'L'},
    '003.13WFM_PLUM_XL': {'design': '003W', 'color': 'PLUM', 'size': 'XL'},
    '0.03.12FM_PINK_XL': {'design': '003W', 'color': 'PINK', 'size': 'XL'},
    '0.03.12FM_PINK_L': {'design': '003W', 'color': 'PINK', 'size': 'L'},
    '0.03.12FM_PINK_M': {'design': '003W', 'color': 'PINK', 'size': 'M'},
    '123.13M_BLACK_XL': {'design': '123M', 'color': 'BLACK', 'size': 'XL'},
    '123.13M_BLACK_L': {'design': '123M', 'color': 'BLACK', 'size': 'L'},
    '123.13M_BLACK_M': {'design': '123M', 'color': 'BLACK', 'size': 'M'},
    'SP_123.1M_YELLOW_L': {'design': '123M', 'color': 'YELLOW', 'size': 'L'},
    'SP_123.1M_YELLOW_M': {'design': '123M', 'color': 'YELLOW', 'size': 'M'},
    'SP_123.1M_YELLOW_XL': {'design': '123M', 'color': 'YELLOW', 'size': 'XL'},
    'SP_123M.24_BLACK_L': {'design': '123M', 'color': 'BLACK', 'size': 'L'},
    'SP_123M.24_BLACK_XL': {'design': '123M', 'color': 'BLACK', 'size': 'XL'},
    'SP_123M.24_BLACK_M': {'design': '123M', 'color': 'BLACK', 'size': 'M'},
}

# Helper function jo View use karega
def get_sku_details(sku):
    # Agar SKU list me hai to details return karo
    if sku in SKU_DICT:
        return SKU_DICT[sku], True # True matlab Mapped hai
    
    # Agar nahi hai to default return karo
    return {
        'design': 'Unmapped',
        'color': '-',
        'size': sku  # Size ki jagah SKU dikha denge taaki pehchan sakein
    }, False # False matlab Unmapped hai