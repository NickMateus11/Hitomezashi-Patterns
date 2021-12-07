import cv2
import numpy as np
import random

def main():
    x_dim, y_dim = 800, 608
    padding = 10

    x_cells = 16
    y_cells = 16
    
    x_step = (x_dim//x_cells)
    y_step = (y_dim//y_cells)

    while True:
        canvas = np.zeros((y_dim+2*padding, x_dim+2*padding), dtype=np.uint8)
        
        input_data_x = [int(random.random()*2) for _ in range(x_cells)]
        input_data_y = [int(random.random()*2) for _ in range(y_cells)]
        
        for x in range(x_cells):
            for y in range(y_cells//2):
                bit = input_data_x[x]
                x_coord = x * x_step
                y_coord = y*(2*y_step) + (bit*y_step)
                cv2.line(canvas, 
                        (x_coord+padding, y_coord+padding), 
                        (x_coord+padding, y_coord+y_step+padding), 
                        (255,)*3, 
                        thickness=1
                    )
        
        for y in range(y_cells):
            for x in range(x_cells//2):
                bit = input_data_y[y]
                x_coord = x*(2*x_step) + (bit*x_step)
                y_coord = y * y_step
                cv2.line(canvas, 
                        (x_coord+padding, y_coord+padding), 
                        (x_coord+x_step+padding, y_coord+padding), 
                        (255,)*3, 
                        thickness=1
                    )

        cv2.rectangle(canvas, (padding, padding), (x_dim+padding, y_dim+padding), (255,)*3, thickness=1)

        cv2.imshow("win", canvas)

        key = cv2.waitKey(0) & 0xFF
        if key == ord('s'):
            print("saving image..")
            print("Success" if cv2.imwrite("images/output.png", canvas) \
                else "Failed..specified path doesn't exist")
        elif key == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()