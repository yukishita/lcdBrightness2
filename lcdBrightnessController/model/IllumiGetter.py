import smbus
import time
import threading
import statistics

class IllumiGetter( object ):
    currentLX = []
    
    """ コンストラクタ """
    def __init__(self) -> None:
        pass

    """ 現在輝度を取得 """
    def getCurrentLX( self ):
        """ まだ十分な値を取得できてない時は Exception """
        if( len(self.currentLX) < 5 ):
            raise ValueError("lx measure not ready")

        """ 過去取得分の平均値を取得 """
        average = statistics.mean( self.currentLX )

        return average

""" Raspberry Pi 用の実装 """
class RaspiIllumiGetter( IllumiGetter ):

    """ I2C読み込み準備 """
    I2CBus = smbus.SMBus(1)
    I2CAddr = 0x23

    def __init__(self) -> None:
        super().__init__()

        """ 輝度取得スレッドの開始 """
        self.thread = threading.Thread(target=self.lxGetThread)
        self.thread.start()

    """ 輝度情報を更新するスレッド """
    def lxGetThread( self ):
        while True:
            """ 輝度の取得 """
            self.currentLX.append( self.readLCDLxBySPI() )

            """ 指定以上取得していたら最も古いデータを削除 """
            if( len(self.currentLX) > 5 ):
                self.currentLX.pop(0)

            """ 指定期間 sleep """
            time.sleep(500/1000)

    """ I2C から輝度を読み込み """
    def readLCDLxBySPI( self ):
        """ 輝度読み込み """
        LxRead = self.I2CBus.read_i2c_block_data( self.I2CAddr, 0x11 )
        Lx = LxRead[1]* 10

        return Lx