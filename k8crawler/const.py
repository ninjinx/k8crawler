class ConstBase:  # 定義値ベース
    # 定数定義
    # 名前が別の名前を含む場合は優先したい名前の値を大きく設定する
    NONE = 0

    # 定義値と値の対応
    const_dict = {}

    @classmethod
    def search(cls, text):
        # 定義値に一致するか検索
        result = cls.NONE
        for k, v in cls.const_dict.items():
            if k in text:
                # 値が大きければ更新（名前が別の名前を含んでいる場合の対策）
                if v > result:
                    result = v

        # 検索結果を返却
        return result


class Track(ConstBase):  # レース場
    # 定数定義
    TRACK_ID_SAPPORO = 1
    TRACK_ID_HAKODATE = 2
    TRACK_ID_FUKUSIMA = 3
    TRACK_ID_NIGATA = 4
    TRACK_ID_TOKYO = 5
    TRACK_ID_NAKAYAMA = 6
    TRACK_ID_TYUKYO = 7
    TRACK_ID_KYOTO = 8
    TRACK_ID_HANSHIN = 9
    TRACK_ID_OGURA = 10

    # 定義値と値の対応
    const_dict = {
        '札幌': TRACK_ID_SAPPORO,
        '函館': TRACK_ID_HAKODATE,
        '福島': TRACK_ID_FUKUSIMA,
        '新潟': TRACK_ID_NIGATA,
        '東京': TRACK_ID_TOKYO,
        '中山': TRACK_ID_NAKAYAMA,
        '中京': TRACK_ID_TYUKYO,
        '京都': TRACK_ID_KYOTO,
        '阪神': TRACK_ID_HANSHIN,
        '小倉': TRACK_ID_OGURA,
    }


class Ground(ConstBase):  # 馬場
    # 定数定義
    GROUND_DIRT = 1
    GROUND_TURF = 2
    GROUND_STEELECHASA = 3

    # 定義値と値の対応
    const_dict = {
        'ダ': GROUND_DIRT,
        '芝': GROUND_TURF,
        '障': GROUND_STEELECHASA,
    }


class GroundCondition(ConstBase):  # 馬場状態
    # 定数定義
    GROUND_CONDITION_FIRM = 1
    GROUND_CONDITION_GOOD = 2
    GROUND_CONDITION_YIELDING = 3
    GROUND_CONDITION_SOFT = 4

    # 定義値と値の対応
    const_dict = {
        '良': GROUND_CONDITION_FIRM,
        '稍重': GROUND_CONDITION_GOOD,
        '重': GROUND_CONDITION_YIELDING,
        '不良': GROUND_CONDITION_SOFT,
    }


class Sex(ConstBase):  # 性別
    # 定数定義
    SEX_STALLION = 1
    SEX_MARE = 2
    SEX_GELDING = 3

    # 定義値と値の対応
    const_dict = {
        '牡': SEX_STALLION,
        '牝': SEX_MARE,
        'セ': SEX_GELDING,
    }


class Clockwise(ConstBase):  # 回り
    # 定数定義
    CLOCK_WISE_RIGHT = 1
    CLOCK_WISE_LEFT = 2
    CLOCK_WISE_STRAIGHT = 3

    # 定義値と値の対応
    const_dict = {
        '右': CLOCK_WISE_RIGHT,
        '左': CLOCK_WISE_LEFT,
        '直線': CLOCK_WISE_STRAIGHT,
    }


class Side(ConstBase):  # 側
    # 定数定義
    SIDE_IN = 1
    SIDE_OUT = 2
    SIDE_OUT_IN = 3
    SIDE_IN_OUT = 4

    # 定義値と値の対応
    const_dict = {
        '内': SIDE_IN,
        '外': SIDE_OUT,
        '外-内': SIDE_OUT_IN,
        '内-外': SIDE_IN_OUT,
    }


class Weather(ConstBase):  # 天候
    # 定数定義
    WEATHER_SUNNY = 1
    WEATHER_CLOUDY = 2
    WEATHER_RAIN = 3
    WEATHER_SNOW = 4

    # 定義値と値の対応
    const_dict = {
        '晴': WEATHER_SUNNY,
        '曇': WEATHER_CLOUDY,
        '雨': WEATHER_RAIN,
        '雪': WEATHER_SNOW,
    }


class AgeCondition(ConstBase):  # 年齢条件
    # 定数定義
    AGE_CONDITION_2_OLD = 1
    AGE_CONDITION_3_OLD = 2
    AGE_CONDITION_OVER_3_OLD = 3
    AGE_CONDITION_OVER_4_OLD = 4

    # 定義値と値の対応
    const_dict = {
        '２歳': AGE_CONDITION_2_OLD,
        '３歳': AGE_CONDITION_3_OLD,
        '３歳以上': AGE_CONDITION_OVER_3_OLD,
        '４歳以上': AGE_CONDITION_OVER_4_OLD,
    }


class Class(ConstBase):  # クラス
    # 定数定義
    CLASS_G1 = 1
    CLASS_G2 = 2
    CLASS_G3 = 3
    CLASS_OP = 4
    CLASS_1600 = 5
    CLASS_1000 = 6
    CLASS_500 = 7
    CLASS_NOVICE = 8
    CLASS_MAIDEN = 9
    CLASS_LISTED = 10

    # 定義値と値の対応
    const_dict = {
        'G1': CLASS_G1,
        'G2': CLASS_G2,
        'G3': CLASS_G3,
        'オープン': CLASS_OP,
        '１６００万': CLASS_1600,
        '１０００万': CLASS_1000,
        '５００万': CLASS_500,
        '新馬': CLASS_NOVICE,
        '未勝利': CLASS_MAIDEN,
        '未出走': CLASS_NOVICE,
        '１勝クラス': CLASS_500,
        '２勝クラス': CLASS_1000,
        '３勝クラス': CLASS_1600,
    }


class TrainingCenter(ConstBase):  # トレセン
    # 定数定義
    TRAINING_CENTER_MIHO = 1
    TRAINING_CENTER_RITTO = 2

    # 定義値と値の対応
    const_dict = {
        '美浦': TRAINING_CENTER_MIHO,
        '栗東': TRAINING_CENTER_RITTO,
    }
