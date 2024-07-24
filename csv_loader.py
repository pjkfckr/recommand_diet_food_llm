import chardet
import pandas as pd


def get_encoding(filename: str) -> str:
    with open(filename, 'rb') as f:
        result = chardet.detect(f.read())

    return result['encoding']


def get_raw_material_food() -> pd.DataFrame:
    encoding = get_encoding('raw_material_food_standard_data.csv')
    df = pd.read_csv('./raw_material_food_standard_data.csv', encoding=encoding)
    df.drop([
        '대표식품코드', '식품기원코드', '식품대분류코드',
        '대표식품코드', '식품중분류코드', '식품소분류코드',
        '식품세분류코드', '식품세분류명', '폐기율(%)',
        '출처코드', '출처명', '원산지국코드', '수입여부',
        '데이터생성방법명', '원산지국명', '원산지역명', '데이터생성방법코드',
        '데이터구분코드', '데이터구분명', '식품코드', '제공기관코드', '제공기관명',
        '데이터기준일자', '생산·채취·포획월', '데이터생성일자'
    ],
        axis=1, inplace=True)
    # text 컬럼 생성
    df['text'] = (
            "식품명: " + df['식품명'] + ", " +
            "식품기원명: " + df['식품기원명'] + ", " +
            "식품대분류명: " + df['식품대분류명'] + ", " +
            "대표식품명: " + df['대표식품명'] + ", " +
            "식품중분류명: " + df['식품중분류명'] + ", " +
            "식품소분류명: " + df['식품소분류명'] + ", " +
            "영양성분함량기준량: " + df['영양성분함량기준량'].astype(str) + ", " +
            "에너지(kcal): " + df['에너지(kcal)'].astype(str) + ", " +
            "수분(g): " + df['수분(g)'].astype(str) + ", " +
            "단백질(g): " + df['단백질(g)'].astype(str) + ", " +
            "지방(g): " + df['지방(g)'].astype(str) + ", " +
            "회분(g): " + df['회분(g)'].astype(str) + ", " +
            "탄수화물(g): " + df['탄수화물(g)'].astype(str) + ", " +
            "당류(g): " + df['당류(g)'].astype(str) + ", " +
            "식이섬유(g): " + df['식이섬유(g)'].astype(str) + ", " +
            "칼슘(mg): " + df['칼슘(mg)'].astype(str) + ", " +
            "철(mg): " + df['철(mg)'].astype(str) + ", " +
            "인(mg): " + df['인(mg)'].astype(str) + ", " +
            "칼륨(mg): " + df['칼륨(mg)'].astype(str) + ", " +
            "나트륨(mg): " + df['나트륨(mg)'].astype(str) + ", " +
            "비타민 A(μg RAE): " + df['비타민 A(μg RAE)'].astype(str) + ", " +
            "레티놀(μg): " + df['레티놀(μg)'].astype(str) + ", " +
            "베타카로틴(μg): " + df['베타카로틴(μg)'].astype(str) + ", " +
            "티아민(mg): " + df['티아민(mg)'].astype(str) + ", " +
            "리보플라빈(mg): " + df['리보플라빈(mg)'].astype(str) + ", " +
            "니아신(mg): " + df['니아신(mg)'].astype(str) + ", " +
            "비타민 C(mg): " + df['비타민 C(mg)'].astype(str) + ", " +
            "비타민 D(μg): " + df['비타민 D(μg)'].astype(str) + ", " +
            "콜레스테롤(mg): " + df['콜레스테롤(mg)'].astype(str) + ", " +
            "포화지방산(g): " + df['포화지방산(g)'].astype(str) + ", " +
            "트랜스지방산(g): " + df['트랜스지방산(g)'].astype(str)
    )

    return df
