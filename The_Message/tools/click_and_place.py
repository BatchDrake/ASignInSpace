import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

SIZE=65536
STRIDE=256
GLOBOFF=0

WIDTH=STRIDE
HEIGHT=SIZE//STRIDE

font = {'family' : 'Calibri',
        'size'   : 13}

matplotlib.rc('font', **font)

bitsfile = '../../Candidates/artifacts/data17square.txt'
data = np.fromfile(bitsfile, dtype = '<i1').astype(float)
curr_offset=0
xor_mode = True
moved = True

bits = data - 48

fftbits  = np.fft.fft(2 * (bits - .5))
bitscorr = np.fft.ifft(fftbits * np.conj(fftbits))

shifts     = []
offsets    = []

sbits = 2 * (bits.copy() - .5)

fig,ax = plt.subplots()

def draw_all():
    global curr_offset
    global xor_mode
    global moved
    
    if xor_mode:
        as_picture = np.ones(bits.shape).reshape(HEIGHT, WIDTH)
        for shift in shifts:
            as_picture *= shift
        as_picture *= -(-1)**len(shifts)  
    else:
        as_picture = np.zeros(bits.shape).reshape(HEIGHT, WIDTH)
        for shift in shifts:
            as_picture += shift + 1
    
    if moved:
        rolled = np.roll(sbits.copy(), curr_offset).reshape(as_picture.shape)
        if xor_mode:
            as_picture *= rolled
            
        else:
            as_picture += rolled + 1
    else:
        if xor_mode:
            as_picture *= -1

    centered = np.roll(as_picture.copy().ravel(), GLOBOFF).reshape(as_picture.shape)

    ax.clear()
    if xor_mode:
        ax.imshow(centered, cmap = 'gray', vmin = -1, vmax = 1)
    else:
        ax.imshow(centered < 1, cmap = 'gray', vmin = 0, vmax = 1)

    if not moved:
        ax.set_title(fr'Offsets: {offsets}')
    else:
        ax.set_title(fr'Offsets: {offsets} + {curr_offset}')

    ax.set_xlabel('Horizontal axis [px]')
    ax.set_ylabel('Vertical axis [px]')

    plt.tight_layout()
    plt.draw()


def onclick(event):
    global curr_offset
    ix, iy = int(event.xdata)-WIDTH//2, int(event.ydata)-HEIGHT//2
    if ix is None or iy is None:
        return
    
    curr_offset = int(ix + iy * 256)
    draw_all()

def on_press(event):
    global curr_offset
    global shifts
    global xor_mode
    global moved
    global offsets
    
    moved = True
    
    if event.key == 'right':
        curr_offset += 1
    elif event.key == 'left':
        curr_offset -= 1
    elif event.key == 'down':
        curr_offset += STRIDE
    elif event.key == 'up':
        curr_offset -= STRIDE
    elif event.key == 'x':
        xor_mode = not xor_mode
    elif event.key == 'enter':
        moved = False
        offsets.append(curr_offset)
        shifts.append(np.roll(sbits.copy(), curr_offset).reshape(HEIGHT, WIDTH))
    elif event.key == 'delete':
        if not len(shifts) == 0:
            shifts  = shifts[0:len(shifts)-1]
            offsets = offsets[0:len(shifts)-1]
            
    draw_all()

fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('key_press_event', on_press)

draw_all()

plt.show()
