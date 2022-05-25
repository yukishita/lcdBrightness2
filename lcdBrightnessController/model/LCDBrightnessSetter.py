import time
import threading

class LCDBrightnessSetter( object ):
    targetBrightness = 255
    currentBrightness = 255

    """ コンストラクタ """
    def __init__(self) -> None:
        """ 輝度取得スレッドの開始 """
        self.thread = threading.Thread(target=self.brightnessSetThread)
        self.thread.start()

    """ 輝度情報を更新するスレッド """
    def brightnessSetThread( self ):
        while True:
            """ ターゲット輝度に変化があるとき輝度を変更 """
            if( self.targetBrightness != self.currentBrightness ):
                if   self.currentBrightness < self.targetBrightness:  self.currentBrightness = self.currentBrightness + 1
                elif self.currentBrightness > self.targetBrightness:  self.currentBrightness = self.currentBrightness - 1
                """ LCD輝度を変更 """
                self.setActualBrightness( self.currentBrightness )

            """ 指定期間 sleep """
            time.sleep(10/1000)

    """ ターゲット輝度を設定 """
    def setTargetBrightness( self, _targetBrightness ):
        self.targetBrightness = _targetBrightness

""" Raspberry Pi 用の実装 """
class RaspiLCDBrightnessSetter( LCDBrightnessSetter ):
    def __init__(self) -> None:
        super().__init__()

        """ 初期輝度で初期化 """
        self.setActualBrightness( self.currentBrightness )

    def setActualBrightness( self, _actualBrightness ):
        f = open('/sys/class/backlight/rpi_backlight/brightness', 'w')
        f.write( str( _actualBrightness ) )
        f.close()
        pass
