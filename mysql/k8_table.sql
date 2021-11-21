CREATE TABLE race_date
(
  date   INT NOT NULL AUTO_INCREMENT COMMENT 'レース開催日',
  year   INT NULL     COMMENT 'レース開催：年',
  month  INT NULL     COMMENT 'レース開催：日',
  is_get INT NULL     DEFAULT 0 COMMENT 'レース結果情報取得フラグ',
  PRIMARY KEY (date)
) COMMENT 'レース日程一覧テーブル';

CREATE TABLE race_horse_info
(
  horse_id        VARCHAR(128) NOT NULL COMMENT '競走馬ID（netkeiba準拠）',
  name            VARCHAR(128) NULL     COMMENT '名前',
  birthday        INT          NULL     COMMENT '誕生日',
  sex             INT          NULL     COMMENT '性別（牡・牝・騙）',
  home            VARCHAR(128) NULL     COMMENT '産地',
  breeder_id      INT          NULL     COMMENT '生産牧場ID（netkeiba準拠）',
  owner_id        INT          NULL     COMMENT '馬主ID（netkeiba準拠）',
  training_center INT          NULL     COMMENT 'トレーニングセンター（美穂・栗東）',
  trainer_id      INT          NULL     COMMENT '調教師ID（netkeiba準拠）',
  father_id       VARCHAR(128) NULL     DEFAULT 0 COMMENT '父',
  mother_id       VARCHAR(128) NULL     DEFAULT 0 COMMENT '母',
  PRIMARY KEY (horse_id)
) COMMENT '競走馬情報';

CREATE TABLE race_horse_result
(
  race_id           BIGINT       NOT NULL COMMENT '管理ID（レース日程+会場ID+レース番号）',
  horse_num         INT          NOT NULL COMMENT '馬番',
  frame_num         INT          NULL     COMMENT '枠番',
  horse_id          VARCHAR(128) NOT NULL COMMENT '競走馬ID（netkeiba準拠）',
  sex               INT          NULL     COMMENT '性別（牡・牝・騙）',
  age               INT          NULL     COMMENT '馬齢',
  horse_weight      INT          NULL     COMMENT '馬体重',
  horse_weight_diff INT          NULL     COMMENT '馬体重差',
  weight            INT          NULL     COMMENT '斤量（kg*10）',
  odds              INT          NULL     COMMENT 'オッズ（odds*10）',
  rank              INT          NULL     COMMENT '順位',
  time              INT          NULL     COMMENT 'タイム（秒*10）',
  popularity        INT          NULL     COMMENT '人気',
  last_3f           INT          NULL     COMMENT '上がり3F（秒*10）',
  jockey_id         INT          NULL     COMMENT '騎手ID（netkeiba準拠）',
  training_center   INT          NULL     COMMENT 'トレーニングセンター（美穂・栗東）',
  trainer_id        INT          NULL     COMMENT '調教師ID（netkeiba準拠）',
  PRIMARY KEY (race_id, horse_num)
) COMMENT '競走馬レース結果情報';

CREATE TABLE race_info
(
  race_id          BIGINT       NOT NULL COMMENT '管理ID（レース日程+会場ID+レース番号）',
  date             INT          NOT NULL COMMENT 'レース開催日',
  track_id         INT          NULL     COMMENT 'レース場ID',
  race_num         INT          NULL     COMMENT 'レース番号',
  entry_num        INT          NULL     COMMENT '出走頭数',
  distance         INT          NULL     COMMENT '距離',
  clockwise        INT          NULL     COMMENT '回り（右・左）',
  side             INT          NULL     COMMENT '側（内・外）',
  ground           INT          NULL     COMMENT '馬場（芝・ダ・障）',
  ground_condition INT          NULL     COMMENT '馬場状態',
  weather          INT          NULL     COMMENT '天候',
  mare_only_flag   INT          NULL     COMMENT '牝馬限定フラグ',
  age_condition    INT          NULL     COMMENT '馬齢条件',
  class_id         INT          NULL     COMMENT 'クラス',
  race_name        VARCHAR(128) NULL     COMMENT 'レース名',
  PRIMARY KEY (race_id)
) COMMENT 'レース基本情報テーブル';