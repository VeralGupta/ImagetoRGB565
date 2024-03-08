import cv2
from tkinter import filedialog
import tempfile
import os
#have to sort it to give clean image and take color approximations acording to surrounding
with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as f:  #temperory notepad
    file_path = filedialog.askopenfilename(title="Open Image File", filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")])
    if file_path !='':
        cb=cv2.imread(file_path,cv2.IMREAD_COLOR)
        desired_width=80  #put the size you want it in (has to be updated to entered by user)
        desired_height=80 #put the size you want it in (has to be updated to entered by user)
        dim=(desired_width,desired_height)
        cb=cv2.resize(cb,dsize=dim,interpolation=cv2.INTER_AREA)
        f.write('const unsigned short myBitmap [] PROGMEM = \n {')
        def changetorgb565(k):
            b,g,r=k
            red_5bit = (r >> 3) & 0x1F  # Shift 3 bits right and mask to keep 5 LSBs
            green_6bit = (g >> 2) & 0x3F  # Shift 2 bits right and mask to keep 6 LSBs
            blue_5bit = b & 0x1F    # Mask to keep 5 LSBs 
            rgb565 = (red_5bit << 11) | (green_6bit << 5) | blue_5bit
            return rgb565
        p,n=0,1
        for x in range(len(cb)):
            for y in range(len(cb[0])):
                if(p<16):
                    p=p+1
                if(p==16):
                    f.write('//('+str(n*16)+') pixels\n')
                    p=1
                    n=n+1
                k=changetorgb565(cb[x,y])
                f.write(f'{k:#06X}'+', ')
        f.write('\n};')
        f.close()
        print("DONE")
    filename = f.name
    if os.name == 'nt': 
      os.startfile(filename)
