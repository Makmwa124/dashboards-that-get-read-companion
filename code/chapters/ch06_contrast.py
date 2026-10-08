# Chapter 6: WCAG contrast ratio of each palette colour against white
def luminance(hex_colour):
    h = hex_colour.lstrip("#")
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]

def contrast(fg, bg="#FFFFFF"):
    l1, l2 = sorted([luminance(fg), luminance(bg)], reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)

for name, hx in [("Dark blue", "#1F4E79"), ("Dark grey", "#4D4D4D"), ("Red", "#C8102E"),
                 ("Mid grey", "#7F7F7F"), ("Light grey", "#BDBDBD")]:
    r = contrast(hx)
    print(f"{name:<11}{hx}  {r:5.2f} : 1  {'normal text OK' if r >= 4.5 else 'large text only' if r >= 3 else 'not for text'}")
