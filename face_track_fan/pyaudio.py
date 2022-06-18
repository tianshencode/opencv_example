import winsound
import time


def play_music():
    winsound.PlaySound('where_are_you', winsound.SND_ASYNC)
    time.sleep(3)


play_music()