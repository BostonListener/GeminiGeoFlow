import re

def parse_coordinate_string(coord_str):
    """Parse coordinate string in various formats to decimal degrees"""
    if not coord_str:
        return None, None
    
    coord_str = coord_str.strip()
    
    parts = [p.strip() for p in coord_str.split(',')]
    if len(parts) != 2:
        return None, None
    
    try:
        lat = parse_single_coordinate(parts[0])
        lon = parse_single_coordinate(parts[1])
        
        if lat is not None and lon is not None:
            return lat, lon
    except:
        pass
    
    return None, None

def parse_single_coordinate(coord_str):
    """Parse a single coordinate value"""
    coord_str = coord_str.strip()
    
    direction = 1
    if coord_str[-1].upper() in ['S', 'W']:
        direction = -1
        coord_str = coord_str[:-1].strip()
    elif coord_str[-1].upper() in ['N', 'E']:
        direction = 1
        coord_str = coord_str[:-1].strip()
    
    coord_str = coord_str.rstrip('°')
    
    dms_pattern = r"(-?\d+)[°\s]+(\d+(?:\.\d+)?)[′'\s]+(\d+(?:\.\d+)?)[″\"]?"
    match = re.match(dms_pattern, coord_str)
    
    if match:
        degrees = float(match.group(1))
        minutes = float(match.group(2))
        seconds = float(match.group(3))
        
        decimal = abs(degrees) + minutes/60 + seconds/3600
        if degrees < 0:
            decimal = -decimal
        
        return decimal * direction
    
    try:
        decimal = float(coord_str)
        return decimal * direction
    except ValueError:
        return None