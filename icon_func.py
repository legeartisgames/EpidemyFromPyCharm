icon_font = 'fonts/Epidemy.ttf'
def get_star_icon(size, coef = 2):
    return " [size="+ str(int(coef*size))+ "]"+"[font="+icon_font+"]Z[/font][/size]"
def get_coin_icon(size, coef = 2):
    return " [size="+ str(int(coef*size))+ "]"+"[font="+icon_font+"]C[/font][/size]"

def letters_to_icons_full(string):
    string = string.replace(" z ", " [font="+icon_font+"]S[/font] (z) ")
    string = string.replace(" d ", " [font="+icon_font+"]R[/font] (d) ")
    
    string = string.replace("z_in", "[font="+icon_font+"]Si[/font] (z_in)")
    string = string.replace("z_out", "[font="+icon_font+"]So[/font] (z_out)")
    string = string.replace("d_out", "[font="+icon_font+"]Ro[/font] (d_out)")
    string = string.replace("d_in", "[font="+icon_font+"]Ri[/font] (d_in)")
    
    string = string.replace(" ill", " [font="+icon_font+"]I[/font] [font=fonts/Verdana.ttf](ill)[/font]" )
    string = string.replace("Ill", "[font="+icon_font+"]I[/font] [font=fonts/Verdana.ttf](Ill)[/font]")
    string = string.replace("dead", "[font="+icon_font+"]D[/font] [font=fonts/Verdana.ttf](dead)[/font]")
    string = string.replace("Dead", "[font="+icon_font+"]D[/font] [font=fonts/Verdana.ttf](Dead)[/font]")
    
    string = string.replace("coins", "[font="+icon_font+"]C[/font] (coins)")
    string = string.replace("coin", "[font="+icon_font+"]C[/font] (coin)")
    string = string.replace("монеты", "[font="+icon_font+"]C[/font] (монеты)")   
    string = string.replace("монету", "[font="+icon_font+"]C[/font] (монету)")    
    string = string.replace("монет", "[font="+icon_font+"]C[/font] (монет)")
    
    return string

def letters_to_icons(string):
    string = string.replace("z_in", "[font="+icon_font+"]Si[/font]")
    string = string.replace("z_out", "[font="+icon_font+"]So[/font](z_out)")
    string = string.replace("d_out", "[font="+icon_font+"]Ro[/font](d_out)")
    string = string.replace("d_in", "[font="+icon_font+"]Ri[/font]")
    string = string.replace("ill", "[font="+icon_font+"]I[/font]")
    string = string.replace("Ill", "[font="+icon_font+"]I[/font]")
    string = string.replace("dead", "[font="+icon_font+"]D[/font]")
    string = string.replace("Dead", "[font="+icon_font+"]D[/font]")
    
    string = string.replace("coins", "[font="+icon_font+"]C[/font]")
    string = string.replace("coin", "[font="+icon_font+"]C[/font]")
    string = string.replace("монеты", "[font="+icon_font+"]C[/font]")   
    string = string.replace("монету", "[font="+icon_font+"]C[/font]")    
    string = string.replace("монет", "[font="+icon_font+"]C[/font]")
    
    
    return string


def add_money_icon(string, size, coef = 2):
    string = string + "[size="+ str(int(coef*size))+ "]"+" [font="+icon_font+"]C[/font][/size]"
    return string
def add_star_icon(string, size, coef = 1.8):
    string = string + " [size="+ str(int(coef*size))+ "]"+" [font="+icon_font+"]Z[/font][/size]"
    return string
def add_money_icon_simple(string):
    string = string +" [font="+icon_font+"]C[/font]"
    return string
def letter_to_icons_increasing_size(size, coef, string):
    string = string.replace(" z ", " [font="+icon_font+"][size="+ str(int(coef*size))+ "]S[/font][/size] (z) ")
    string = string.replace(" d ", " [font="+icon_font+"][size="+ str(int(coef*size))+ "]R[/font][/size] (d) ")
    
    string = string.replace("z_in", "[font="+icon_font+"][size="+ str(int(coef*size))+ "]Si[/font][/size] [font_features=bold](z_in)[/font_features]")
    string = string.replace("z_out", "[font="+icon_font+"][size="+ str(int(coef*size))+ "]So[/font][/size]  (z_out)")
    string = string.replace("d_out", "[font="+icon_font+"][size="+ str(int(coef*size))+ "]Ro[/font][/size]  (d_out)")
    string = string.replace("d_in", "[font="+icon_font+"][size="+ str(int(coef*size))+ "]Ri[/font][/size]  (d_in)")
    
    string = string.replace(" ill", " [font="+icon_font+"][size="+ str(int(coef*size))+ "]I[/font][/size]  (ill)" )
    string = string.replace("Ill", "[font="+icon_font+"][size="+ str(int(coef*size))+ "]I[/font][/size]  (Ill)")
    string = string.replace("dead", "[font="+icon_font+"][size="+ str(int(coef*size))+ "]D[/font][/size]  (dead)")
    string = string.replace("Dead", "[font="+icon_font+"][size="+ str(int(coef*size))+ "]D[/font][/size]  (Dead)")
    
    string = string.replace("coins", "[size="+ str(int(coef*size))+"][font="+icon_font+"]C[/font][/size]")
    string = string.replace("coin", "[size="+ str(int(coef*size))+ "][font="+icon_font+"]C[/font][/size]")
    string = string.replace("монеты", "[size="+ str(int(coef*size))+ "]"+"[font="+icon_font+"]C[/font][/size]")   
    string = string.replace("монету", "[font="+icon_font+"][size="+ str(int(coef*size))+ "]C[/font][/size]")    
    string = string.replace("монет", "[font="+icon_font+"][size="+ str(int(coef*size))+ "]C[/font][/size]")
    
    string = string.replace("stars", "[size="+ str(int(coef*size))+ "]"+"[font="+icon_font+"]Z[/font][/size]")    
    string = string.replace(" star ", " [size="+ str(int(coef*size))+ "]"+"[font="+icon_font+"]Z[/font][/size] ")
    string = string.replace("sstar", "[size="+ str(int(coef*size))+ "]"+"[font="+icon_font+"]Z[/font][/size] ")
    
    return string