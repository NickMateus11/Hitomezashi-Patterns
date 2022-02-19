import cv2
import numpy as np
import random
import skimage.segmentation as skimage


def hitomezashi(seq_x, seq_y, x_dim, y_dim, padding=10):
    canvas = np.ones((y_dim+2*padding, x_dim+2*padding), dtype=np.uint8) * 255

    x_num = len(seq_x)
    y_num = len(seq_y)
    
    x_step = (x_dim//x_num)
    y_step = (y_dim//y_num)
    
    for x in range(x_num):
        for y in range(y_num//2):
            bit = seq_x[x]
            x_coord = x * x_step
            y_coord = y*(2*y_step) + (bit*y_step)
            cv2.line(canvas, 
                    (x_coord+padding, y_coord+padding), 
                    (x_coord+padding, y_coord+y_step+padding), 
                    (0,)*3, 
                    thickness=1
                )
    
    for y in range(y_num):
        for x in range(x_num//2):
            bit = seq_y[y]
            x_coord = x*(2*x_step) + (bit*x_step)
            y_coord = y * y_step
            cv2.line(canvas, 
                    (x_coord+padding, y_coord+padding), 
                    (x_coord+x_step+padding, y_coord+padding), 
                    (0,)*3, 
                    thickness=1
                )

    cv2.rectangle(canvas, (padding, padding), (x_num*x_step+padding, y_num*y_step+padding), (0,)*3, thickness=1)
    
    return canvas

def random_pattern():
    x_dim, y_dim = 800, 600

    x_cells = 16
    y_cells = 16

    while True:
        input_data_x = [int(random.random()*2) for _ in range(x_cells)]
        input_data_y = [int(random.random()*2) for _ in range(y_cells)]
        
        canvas = hitomezashi(input_data_x, input_data_y, x_dim, y_dim)        
        cv2.imshow("win", canvas)

        key = cv2.waitKey(0) & 0xFF
        if key == ord('s'):
            print("saving image..")
            print("Success" if cv2.imwrite("images/output.png", canvas) \
                else "Failed..specified path doesn't exist")
        elif key == ord('q'):
            break

    cv2.destroyAllWindows()

def flood_fill(img, colours, x_cells, y_cells, padding):
    c_idx = 0
    cell_width, cell_height = len(img[0])//x_cells, len(img)//y_cells
    for i in range(y_cells):
        for j in range(x_cells):
            x,y = j*cell_width+padding + cell_width//2, i*cell_height+padding + cell_height//2

            if j!=0 and tuple(img[y][x]) == colours[c_idx%len(colours)][::-1] \
                or (i!=0 and j==0 and tuple(img[y-cell_height][x]) == colours[c_idx%len(colours)][::-1]): # next fill colour is same as current cell
                c_idx += 1
            
            if tuple(img[y][x]) == (255,)*3:
                mask = skimage.flood(img[..., 0], (y,x))
                img[mask] = colours[c_idx%len(colours)][::-1] # BGR
                c_idx += 1
                # cv2.circle(img, (x,y), 3, colours[c_idx%len(colours)][::-1], thickness=-1)
            # cv2.imshow("window", img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
    return img

def message_pattern(msg_x,msg_y):
    if len(msg_x)>len(msg_y):
        x_dim, y_dim = int(len(msg_x)/len(msg_y) * 800), 800
    else:
        x_dim, y_dim = 800, int(len(msg_y)/len(msg_x) * 800)
    
    bin_msg_x = []
    bin_msg_y = []
    for char in msg_x:
        bits_x = bin(ord(char)).split('b')[1]
        bin_msg_x += [int(bit) for bit in ([0]*(8-len(bits_x)) + list(bits_x))]
    for char in msg_y:
        bits_y = bin(ord(char)).split('b')[1]
        bin_msg_y += [int(bit) for bit in ([0]*(8-len(bits_y)) + list(bits_y))]

    input_data_x = bin_msg_x
    input_data_y = bin_msg_y
        
    canvas = hitomezashi(input_data_x, input_data_y, x_dim, y_dim)
    canvas = cv2.cvtColor(canvas, cv2.COLOR_GRAY2BGR)        
    # cv2.imshow("win", canvas)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # cv2.imwrite(f"images/{msg_x}-{msg_y}.png", canvas)
    return canvas, len(input_data_x), len(input_data_y)

def main():

    img, x_cells, y_cells = message_pattern("HELLO", "WORLD")
    img = flood_fill(img, [(77,200,240), (154,105, 228)], x_cells, y_cells, padding=10)  
 
    cv2.imshow("window", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()