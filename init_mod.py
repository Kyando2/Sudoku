import pyglet.shapes as shapes

def create_shapes(itemslist, WIDTHSIZE, HEIGHTSIZE, color):
    SPACING=10
    ROWS=9
    COLUMNS=9
    SHAPEWIDTH = (-(COLUMNS*SPACING)-(SPACING)+WIDTHSIZE)/COLUMNS
    SHAPEHEIGHT = (-(ROWS*SPACING)-(SPACING)+HEIGHTSIZE)/ROWS
    DISTANCE_X = SHAPEWIDTH + SPACING
    DISTANCE_Y = SHAPEHEIGHT + SPACING
    magic_list = []
    matrice = {} #INDEX (0,0) TO INDEX [COLUMNS, ROWS]
    current_x, current_y = SPACING, SPACING
    for i in range(COLUMNS):
        for j in range(ROWS):
            newshape = shapes.Rectangle(x=current_x, y=current_y, width=SHAPEWIDTH, height=SHAPEHEIGHT, color=color)
            magic_shape = None
            magic_shape2 = None
            if i == 2 or i == 5:
                magic_shape = shapes.Rectangle(x=current_x+SHAPEWIDTH, y=current_y, width=SPACING, height=SHAPEHEIGHT, color=(255,255,255))
            if j == 2 or j == 5:
                magic_shape2 = shapes.Rectangle(x=current_x, y=current_y+SHAPEHEIGHT, width=SHAPEWIDTH, height=SPACING, color=(255,255,255))
            if magic_shape:
                magic_list.append(magic_shape)
            if magic_shape2:
                magic_list.append(magic_shape2)
            itemslist.append(newshape)
            matrice[(i, j)] = newshape
            current_y += DISTANCE_Y
        current_y = SPACING
        current_x += DISTANCE_X
    return matrice, magic_list
