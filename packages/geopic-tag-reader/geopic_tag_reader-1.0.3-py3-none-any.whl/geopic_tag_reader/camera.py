from typing import Optional, Dict, List

# List of equirectangular cameras (make, model)
# https://en.wikipedia.org/wiki/List_of_omnidirectional_(360-degree)_cameras
EQUIRECTANGULAR_MODELS: Dict[str, List[str]] = {
    "Panono": ["Panono"],
    "Vuze": ["Vuze"],
    "Vuze+": ["Vuze+"],
    "BUBL": ["Bublcam"],
    "Ricoh": ["Theta", "Theta m15", "Theta S", "Theta SC", "Theta SC2", "Theta V", "Theta Z1"],
    "Insta360": ["4K", "Nano", "Air", "One", "Pro", "One X", "One R", "X3", "Titan"],
    "Samsung": ["Gear360"],
    "LG": ["360 CAM"],
    "MadV": ["Madventure 360"],
    "Nikon": ["Keymission 360"],
    "Xiaomi": ["米家全景相机"],
    "小蚁(YI)": ["小蚁VR全景相机"],
    "Giroptic iO": ["Giroptic iO"],
    "Garmin": ["Virb 360"],
    "Nokia": ["OZO"],
    "Z Cam": ["S1 Pro", "V1 Pro"],
    "Rylo": ["Rylo"],
    "GoPro": ["Fusion", "Max"],
    "FXG": ["SEIZE", "FM360 Duo"],
}


def is_360(make: Optional[str], model: Optional[str]) -> bool:
    """
    Checks if given camera is equirectangular (360°) based on its make and model.

    >>> is_360(None, None)
    False
    >>> is_360("GoPro", None)
    False
    >>> is_360("GoPro", "Max 360")
    True
    """

    if not make or not model:
        return False

    return any(model.startswith(potentialModel) for potentialModel in EQUIRECTANGULAR_MODELS.get(make, []))
