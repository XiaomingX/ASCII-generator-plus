def get_general_charset():
    return {
        "simple": "@%#*+=-:. ",
        "complex": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    }

def get_chinese_charset():
    return {
        "standard": "龘䶑瀰幗獼鑭躙䵹觿䲔釅欄鐮䥯鶒獭鰽襽螻鰱蹦屭繩圇婹歜剛屧磕媿慪像僭堳噞呱棒偁呣塙唑浠唼刻凌咄亟拮俗参坒估这聿布允仫忖玗甴木亪女去凸五圹亐囗弌九人亏产斗丩艹刂彳丬了５丄三亻讠厂丆丨１二宀冖乛一丶、"
    }

def get_korean_charset():
    return {
        "standard": "ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎㅏㅑㅓㅕㅗㅛㅜㅠㅡㅣ"
    }

def get_japanese_charset():
    return {
        "hiragana": "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん",
        "katakana": "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
    }

def get_english_charset():
    return {
        "standard": "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
    }

def get_russian_charset():
    return {
        "standard": "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя"
    }

def get_german_charset():
    return {
        "standard": "AaÄäBbßCcDdEeFfGgHhIiJjKkLlMmNnOoÖöPpQqRrSsTtUuÜüVvWwXxYyZz"
    }

def get_french_charset():
    return {
        "standard": "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZzÆæŒœÇçÀàÂâÉéÈèÊêËëÎîÎïÔôÛûÙùŸÿ"
    }

def get_spanish_charset():
    return {
        "standard": "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZzÑñáéíóú¡¿"
    }

def get_italian_charset():
    return {
        "standard": "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZzÀÈàèéìòù"
    }

def get_portuguese_charset():
    return {
        "standard": "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZzàÀáÁâÂãÃçÇéÉêÊíÍóÓôÔõÕúÚ"
    }

def get_polish_charset():
    return {
        "standard": "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpRrSsTtUuWwYyZzĄąĘęÓóŁłŃńŻżŚśĆćŹź"
    }

def main():
    charsets = {
        "General": get_general_charset(),
        "Chinese": get_chinese_charset(),
        "Korean": get_korean_charset(),
        "Japanese": get_japanese_charset(),
        "English": get_english_charset(),
        "Russian": get_russian_charset(),
        "German": get_german_charset(),
        "French": get_french_charset(),
        "Spanish": get_spanish_charset(),
        "Italian": get_italian_charset(),
        "Portuguese": get_portuguese_charset(),
        "Polish": get_polish_charset(),
    }
    
    # 打印所有字符集
    for language, charset in charsets.items():
        print(f"{language} Character Set:")
        for key, value in charset.items():
            print(f"  {key}: {value}")
        print()

if __name__ == "__main__":
    main()