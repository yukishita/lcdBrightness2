import time

import lcdBrightnessController.model.IllumiGetter
import lcdBrightnessController.model.LCDBrightnessSetter

class LCDController(object):
    """ コンストラクタ """
    def __init__(self) -> None:
        pass

""" Raspberry Pi 用の実装 """
class RaspiLCDController( LCDController ):

    """ 明るさ取得クラスと輝度設定クラスを定義 """
    illumi = lcdBrightnessController.model.IllumiGetter.RaspiIllumiGetter()
    lcd = lcdBrightnessController.model.LCDBrightnessSetter.RaspiLCDBrightnessSetter()

    """ 明るさ:輝度 テーブル (輝度, LCD輝度) """
    BrightnessTable = [   # 輝度, LCD輝度
        [ 0, 10 ],
        [ 50, 30 ],
        [ 100, 100 ]
    ]

    def __init__(self) -> None:
        super().__init__()

    def startLcdControl( self ):
        while True:
            try:
                """ 輝度を取得してターゲット輝度を取得 """
                targetBrightness = 255
                Lx = self.illumi.getCurrentLX()
                for i in self.BrightnessTable:
                    if Lx <= i[0]:
                        targetBrightness = i[1] 
                        break
                self.lcd.setTargetBrightness( targetBrightness )

            except ValueError:
                pass

            time.sleep(1)