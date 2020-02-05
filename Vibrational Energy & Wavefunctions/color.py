#Written by Gary Zeri, Computer Science Student at Chapman University and Member of the LaRue CatLab
#Color Class to handle picking unique random colors for Plotly
#Color List was retrived from https://community.plot.ly/t/plotly-colours-list/11730/3
colors = [
     'wheat', 'aqua', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond',
     'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral',        
     'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 
     'darkgrey', 'darkgreen', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 
     'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey',     
     'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dodgerblue', 'firebrick',
     'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green',
     'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender',  
     'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan',   
     'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen',
     'lightskyblue', 'lightslategray', 'yellow', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 
     'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 
     'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 
     'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive',
     'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise',
     'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple',
     'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 
     'silver', 'skyblue', 'slateblue', 'slategrey', 'springgreen', 'steelblue', 'mediumpurple', 'tan', 
    'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'blue', 'red'
]

usedColors = []

def getColor():
    
    usedColors.append(colors.pop())
    
    #in the case where all the colors have been used once
    if(colors == []):
        colors.extend(usedColors)
        usedColors.clear()
    
    return usedColors[-1]