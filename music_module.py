from kivy.core.audio import SoundLoader, Sound
from kivy.uix.switch import Switch
import common_data
sound = 0 

from kivy.utils import platform
print(platform)
if platform == "android":
    
    from jnius import autoclass

    MediaPlayer = autoclass("android.media.MediaPlayer")
    FileInputStream = autoclass("java.io.FileInputStream")
    AudioManager = autoclass("android.media.AudioManager")


class SoundAndroidPlayer(Sound):
    @staticmethod
    def extensions():
        return ("mp3", "mp4", "aac", "3gp", "flac", "mkv", "wav", "ogg")

    def __init__(self, **kwargs):
        self._mediaplayer = None
        super(SoundAndroidPlayer, self).__init__(**kwargs)

    def load(self, filename, looping):
        self.unload()
        self._mediaplayer = MediaPlayer()
        self._mediaplayer.setLooping(looping)
        self._mediaplayer.setAudioStreamType(AudioManager.STREAM_MUSIC)
        self._mediaplayer.setDataSource(filename)
        self._mediaplayer.prepare()

    def unload(self):
        self.stop()
        self._mediaplayer = None

    def pause(self):
        if not self._mediaplayer:
            return
        self._mediaplayer.pause()
        
    def play(self):
        if not self._mediaplayer:
            return
        self._mediaplayer.start()
        super(SoundAndroidPlayer, self).play()

    def stop(self):
        if not self._mediaplayer:
            return
        self._mediaplayer.reset()

    def seek(self, position):
        if not self._mediaplayer:
            return
        self._mediaplayer.seekTo(float(position))

    def get_pos(self):
        if self._mediaplayer:
            return self._mediaplayer.getCurrentPosition() / 1000.
        return super(SoundAndroidPlayer, self).get_pos()

    def on_volume(self, instance, volume):
        if self._mediaplayer:
            volume = float(volume)
            self._mediaplayer.setVolume(volume, volume)

    def _get_length(self):
        if self._mediaplayer:
            return self._mediaplayer.getDuration() / 1000
        return super(SoundAndroidPlayer, self)._get_length()

if platform == "android":
    SoundLoader.register(SoundAndroidPlayer)

music_switches = []

class My_switch(Switch):
    def __init__(self, **kwargs): 
        super(My_switch, self).__init__(**kwargs) 
        global music_switches
        music_switches.append(self)
        self.active = common_data.my_stats.is_music_playing

        self.bind(active = self.callback)
    
    
    def callback(self, value, instance):
        global music_switches
        if common_data.my_stats.is_music_playing == True:
            print("music turned off")
            if platform == "android":
                sound.pause()
            else:
                sound.stop()
            for i in music_switches:
                i.active = False
            
            common_data.my_stats.is_music_playing = False
        else:
            print("music turned on")
            for i in music_switches:
                i.active = True
            sound.play()
            common_data.my_stats.is_music_playing = True
        
        common_data.my_stats.save_to_file()
                
                
    
    @staticmethod
    def load_and_play_music(name='music_new', loop = True):
        if name == 'music_new':
            global sound
        if platform != "android":
            sound2 = SoundLoader.load(filename = 'sounds/'+name+'.ogg')
        else:
            sound2 = SoundAndroidPlayer()
            sound2.load(filename='sounds/'+name+'.ogg', looping=loop)
        if common_data.my_stats.is_music_playing == True:
            sound2.play()
            sound2.volume = common_data.my_stats.volume_of_music
            print("play", name)
            
        sound2.loop = loop
        if name == 'music_new':
            sound = sound2        
My_switch.load_and_play_music()