# Pocket Scarface
# rev 1 - oct 2021 - shabaz
import board
import audiomp3
import audiobusio
import digitalio
import time

# file names
fnames = ["1.mp3", "2.mp3", "3.mp3", "4.mp3", "5.mp3", "6.mp3"]
# buttons
input_gpio = [board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP6]
buttons = []
# other variables
forever = 1

# main program
def main():
    global buttons
    print("Hello")
    # setup connections
    # create I2S output, pins order: (BCLK, FS, DATA)
    i2s = audiobusio.I2SOut(board.GP14, board.GP15, board.GP13)
    # board LED
    boardled = digitalio.DigitalInOut(board.GP25)
    boardled.direction = digitalio.Direction.OUTPUT
    # buttons
    for idx, v in enumerate(input_gpio):
        buttons.append(digitalio.DigitalInOut(v))
        buttons[idx].direction = digitalio.Direction.INPUT
        buttons[idx].pull = digitalio.Pull.UP

    # create MP3 decoder with any file
    dummy = open(fnames[0], "rb")
    asource = audiomp3.MP3Decoder(dummy)

    while forever:
        for idx, b in enumerate(buttons):
            if b.value is False:  # button is pressed
                asource.file = open(fnames[idx], "rb")
                start = time.monotonic()
                i2s.play(asource)  # play the audio source
                while i2s.playing:
                    pass
                stop = time.monotonic()
                print(f"Played {fnames[idx]} {stop - start} sec")


main()  # run main program
