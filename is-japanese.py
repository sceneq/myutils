#!/usr/bin/env python3
# coding: utf-8

"""日本人"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import date


@dataclass
class Human:
    # 出生・親族・婚姻
    父国籍: str
    母国籍: str
    出生地: str
    出生日: date
    父母婚姻関係: bool = True

    # 認知（第3条）
    認知済: bool = False
    認知日: date | None = None
    認知時父日本国民: bool = False  # 出生時 or 死亡時に日本国民
    認知時父現日本国民: bool = False  # 現に日本国民 or 死亡時に日本国民

    # 帰化
    帰化許可日: date | None = None
    日本在留年数: int = 0
    年齢: int = 0
    本国法行為能力: bool = True
    素行善良: bool = True
    生計維持: bool = True
    外国籍保有: bool = False
    外国籍取得後喪失義務: bool = True
    憲法暴力破壊歴: bool = False
    特別事情: bool = False

    日本国民の子: bool = False
    親日本出生: bool = False
    旧日本国籍保持者の子: bool = False  # 第6条第1号
    日本国民の配偶者: bool = False
    継続婚姻年数: int = 0
    日本国民の養子: bool = False
    養子縁組年数: int = 0
    養子縁組時未成年: bool = False
    旧日本国籍保持者: bool = False
    帰化後喪失者: bool = False  # 第8条第3号除外
    無国籍出生: bool = False
    特別功労: bool = False
    国会承認: bool = False
    現住所日本: bool = False

    # 国籍喪失・離脱・重国籍
    国籍喪失_志望取得: bool = False
    国籍喪失_離脱届: bool = False
    国籍喪失_不選択: bool = False

    # 再取得・留保（第12条・第17条）
    国籍再取得日: date | None = None
    国籍留保届提出: bool = True
    父母不詳無国籍: bool = False
    出生時外国籍取得: bool = False  # 出生地主義等で外国籍取得

    # 重国籍（第14条）
    重国籍保有: bool = False
    重国籍取得日: date | None = None
    日本国籍選択届提出: bool = False


def kika_kyoka(h: Human) -> bool:
    # 第5条 一般帰化
    if (
        h.現住所日本
        and h.日本在留年数 >= 5
        and h.年齢 >= 20
        and h.本国法行為能力
        and h.素行善良
        and h.生計維持
        and (not h.外国籍保有 or h.外国籍取得後喪失義務)
        and not h.憲法暴力破壊歴
    ):
        return True

    # 第5条第2項 特別事情
    if h.特別事情:
        return True

    # 第6条 簡易帰化（住所要件緩和）
    if h.現住所日本 and (
        (h.旧日本国籍保持者の子 and h.日本在留年数 >= 3)  # 第1号
        or (h.出生地 == "Japan" and h.日本在留年数 >= 3)  # 第2号前段
        or (h.親日本出生 and h.日本在留年数 >= 3)  # 第2号後段
        or (h.日本在留年数 >= 10)  # 第3号
    ):
        return True

    # 第7条 配偶者帰化（住所・年齢・能力要件緩和）
    if (
        h.日本国民の配偶者
        and h.現住所日本
        and (
            (h.日本在留年数 >= 3)  # 前段: 婚姻期間不問
            or (h.継続婚姻年数 >= 3 and h.日本在留年数 >= 1)  # 後段
        )
    ):
        return True

    # 第8条 その他特例（住所・年齢・生計要件緩和）
    if h.現住所日本:
        if h.日本国民の子:  # 第1号
            return True
        if h.日本国民の養子 and h.養子縁組年数 >= 1 and h.養子縁組時未成年:  # 第2号
            return True
        if h.旧日本国籍保持者 and not h.帰化後喪失者:  # 第3号（帰化後喪失を除く）
            return True
        if h.無国籍出生 and h.日本在留年数 >= 3:  # 第4号
            return True

    # 第9条 特別功労（全要件免除）
    if h.特別功労 and h.国会承認:
        return True

    return False


def is_japanese(h: Human) -> bool:
    today = date.today()

    # 第11条・第13条 国籍喪失
    if h.国籍喪失_志望取得 or h.国籍喪失_離脱届 or h.国籍喪失_不選択:
        return False

    # 第17条 国籍再取得
    if h.国籍再取得日:
        return True

    # 第2条 出生による取得
    if h.父国籍 == "Japanese" or h.母国籍 == "Japanese":
        # 第2条第1号: 父母婚姻関係なしで父のみ日本国民の場合は認知必須
        if (
            not h.父母婚姻関係
            and h.父国籍 == "Japanese"
            and h.母国籍 != "Japanese"
            and not h.認知済
        ):
            return False

        # 第12条 国籍留保: 国外出生で外国籍も取得した場合
        if h.出生地 != "Japan" and h.出生時外国籍取得 and not h.国籍留保届提出:
            return False

        return True

    # 第2条第3号 遺棄児推定
    if h.父母不詳無国籍 and h.出生地 == "Japan":
        return True

    # 第3条 認知による取得
    if h.認知済 and h.認知日:
        age_at_recognition = (h.認知日 - h.出生日).days // 365
        if age_at_recognition < 20 and h.認知時父日本国民 and h.認知時父現日本国民:
            return True

    # 第4条・第10条 帰化による取得
    if h.帰化許可日:
        return True

    # 第14条・第15条 重国籍の選択義務
    if h.重国籍保有 and h.重国籍取得日:
        age_at_acquisition = (h.重国籍取得日 - h.出生日).days // 365

        # 選択期限計算
        if age_at_acquisition < 20:
            # 20歳前取得 → 22歳まで
            limit = date(h.出生日.year + 22, h.出生日.month, h.出生日.day)
        else:
            # 20歳以降取得 → 2年以内
            limit = date(
                h.重国籍取得日.year + 2, h.重国籍取得日.month, h.重国籍取得日.day
            )

        # 期限内に選択届なし → 喪失（催告後）
        if not h.日本国籍選択届提出 and today > limit:
            # 実際は第15条の催告が必要だが簡略化
            return False

        if h.日本国籍選択届提出:
            return True

    return False
