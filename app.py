import streamlit as st
import FinanceDataReader as fdr
import pandas as pd
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(
    page_title="시장 대비 강세 종목 스크리너",
    page_icon="📈",
    layout="wide"
)

st.title("📈 국내 주식 및 ETF 상대 강세(Relative Strength) 스크리너")
st.markdown("원하는 대상과 분석 기간을 선택하여 코스피(KOSPI) 지수 대비 아웃퍼폼한 종목 및 ETF를 발굴하세요.")

# 1. 전체 종목 리스트 (국내개별기업 200 및 기존 TIGER/KODEX ETF)
DOMESTIC_STOCKS = [
    "005930", "000660", "373220", "207940", "005380", "000270", "068270", "105560", "005490", "035420",
    "055550", "028260", "012330", "006400", "035720", "086790", "051910", "032830", "329180", "012450",
    "138040", "066570", "259960", "247540", "196170", "086520", "000810", "034730", "034020", "003670",
    "010130", "033780", "015760", "316140", "009540", "009150", "017670", "011200", "042660", "024110",
    "030200", "003550", "047050", "267260", "352820", "010950", "003490", "018260", "096770", "005830",
    "086280", "180640", "071050", "011070", "010140", "323410", "032640", "326030", "090430", "302440",
    "088980", "006800", "241560", "000100", "011790", "000720", "009830", "021240", "036570", "476080",
    "277810", "028300", "003230", "298040", "047810", "079550", "272210", "064350", "078930", "016360",
    "005940", "039490", "097950", "271550", "035250", "004020", "011780", "161390", "128940", "042700",
    "058470", "036930", "450080", "214150", "145020", "000250", "440110", "141080", "365550", "240810",
    "039030", "403870", "005290", "067310", "000150", "006260", "010120", "267250", "443060", "036460",
    "028670", "000120", "011170", "282330", "007070", "139480", "023530", "008770", "383220", "069960",
    "004170", "030000", "253450", "035900", "041510", "122870", "263750", "251270", "377300", "293490",
    "112040", "012510", "053800", "034230", "114090", "002790", "192820", "161890", "112610", "000880",
    "010060", "375500", "006360", "047040", "294870", "002380", "108320", "000990", "195870", "353200",
    "222800", "007810", "007660", "166090", "064760", "348210", "140910", "137400", "078600", "121600",
    "066970", "348370", "278280", "365340", "107600", "214370", "086900", "085660", "003850", "069620",
    "185750", "008930", "006280", "001060", "237690", "214390", "086430", "007570", "111770", "105630",
    "081660", "001680", "004370", "007310", "005300", "000080", "005180", "267980", "011210", "018880",
    "005850", "010690", "200880", "015750", "012200", "009900", "004410", "002350", "073240"
]

# 2. 첨부 파일별 개별 ETF 종목 리스트 정의
ETF_FILE_1 = [
    "192090", "245360", "117690", "365040", "228820", "232080", "277650", "277640", "277630", "252000", 
    "292160", "292150", "289480", "310960", "310970", "102110", "166400", "289260", "289250", "0204S0", 
    "461580", "496080", "105010", "453870", "133690", "245340", "360750", "143850", "0238P0", "418660", 
    "429010", "435420", "0223R0", "488500", "448290", "448300", "441680", "241180", "195920", "195930"
] # 국가별 대표지수[cite: 6]

ETF_FILE_2 = [
    "0190Y0", "0241R0", "381180", "396500", "396520", "480310", "453950", "0233J0", "466950", "0177R0", 
    "471760", "0053L0", "0117V0", "0148J0", "491010", "0067Y0", "0102A0", "465660", "449690", "491830", 
    "497570", "0142D0", "0123G0", "376410", "396510", "377990", "417630", "404540", "0091P0", "365000", 
    "364990", "400970", "371450", "412770", "300610", "418670", "364980", "394670", "387280", "394660", 
    "371460", "305540", "462010", "0067V0", "447770", "449680", "371470", "364970", "476690", "0168K0", 
    "371160", "364960", "387270", "275980", "381170", "414780", "493810", "472160", "472170", "0047A0", 
    "463250", "464930", "464310", "490090"
] # 혁신성장테마[cite: 10]

ETF_FILE_3 = [
    "203780", "0183J0", "458730", "0015K0", "494840", "248270", "479730", "269370", "276000", "0060H0", 
    "0133E0", "139270", "091220", "139230", "139280", "143860", "157490", "139250", "157500", "091230", 
    "227540", "227550", "228800", "237440", "210780", "261060", "228810", "315270", "307510", "307520", 
    "138540", "147970", "227560", "261140", "138520", "138530", "139220", "139240", "228790", "211560", 
    "150460", "139260", "261070", "494670", "174350", "139290", "227570"
] # 국가별 섹터[cite: 7]

ETF_FILE_4 = [
    "289480", "166400", "482730", "458750", "486290", "0104N0", "0104P0", "493810", "0000D0", "474220", 
    "441680", "0008S0", "458760", "245350", "429000", "0052D0", "472150", "466940", "445910", "465670", 
    "357870", "499660", "440340", "456610", "475630", "449170", "480260", "0094K0", "0192Z0", "157450", 
    "272580", "305080", "329750", "438330", "302190", "182490", "114820", "451530", "0043B0", "0046A0", 
    "0139F0", "476550", "458250", "458260", "451540", "237440", "0025N0", "447770"
] # 안전형인컴형[cite: 8]

ETF_FILE_5 = [
    "139320", "0189B0", "319640", "137610", "160580", "130680", "0072R0", "292560", "182480", "329200", 
    "341850", "0086B0", "0086C0"
] # 원자재부동산통화[cite: 9]

# 3. 전체 통합 ETF 리스트 (5개 파일의 중복 제거 합집합)
ALL_ETFS = list(set(ETF_FILE_1 + ETF_FILE_2 + ETF_FILE_3 + ETF_FILE_4 + ETF_FILE_5))

# --- UI 레이아웃 구성 ---

# 섹션 1: 전체 (주식+ETF) 스크리닝 영역
st.subheader("📊 전체 종목 (주식 + ETF) 스크리너")
col1, col2, col3, col4 = st.columns(4)

with col1:
    btn_all = st.button("🚀 전체기간 (주식+ETF)", type="primary")
with col2:
    btn_short = st.button("⚡ 단기 10·30일 (주식+ETF)", type="secondary")
with col3:
    btn_mid = st.button("🔍 중기 50·100일 (주식+ETF)", type="secondary")
with col4:
    btn_long = st.button("🐢 장기 200일 (주식+ETF)", type="secondary")

st.markdown("---")

# 섹션 2: 전체 통합 ETF 전용 스크리닝 영역
st.subheader("🎯 전체 ETF 통합 전용 스크리너 (5개 파일 전체 통합)")
ecol1, ecol2, ecol3, ecol4 = st.columns(4)

with ecol1:
    e_btn_all = st.button("🚀 전체기간 (통합ETF)")
with ecol2:
    e_btn_short = st.button("⚡ 단기 10·30일 (통합ETF)")
with ecol3:
    e_btn_mid = st.button("🔍 중기 50·100일 (통합ETF)")
with ecol4:
    e_btn_long = st.button("🐢 장기 200일 (통합ETF)")

st.markdown("---")

# 섹션 3: 각 파일별 개별 검색 버튼 영역
st.subheader("📂 파일별 개별 ETF 그룹 검색 (전체 기간 10~200일 기준)")
fcol1, fcol2, fcol3, fcol4, fcol5 = st.columns(5)

with fcol1:
    btn_f1 = st.button("📁 1. 국가별 대표지수")
with fcol2:
    btn_f2 = st.button("📁 2. 혁신성장테마")
with fcol3:
    btn_f3 = st.button("📁 3. 국가별 섹터")
with fcol4:
    btn_f4 = st.button("📁 4. 안전형인컴형")
with fcol5:
    btn_f5 = st.button("📁 5. 원자재·부동산·통화")


# 공통 실행 함수
def run_screener(selected_periods, target_list, title_prefix):
    max_p = max(selected_periods)
    start_date = (datetime.now() - timedelta(days=max_p + 150)).strftime('%Y-%m-%d')
    
    with st.spinner(f"코스피 지수 데이터 및 [{title_prefix}] 수익률을 분석 중입니다... 잠시만 기다려주세요."):
        df_kospi = fdr.DataReader('KS11', start_date)
        
        kospi_returns = {}
        if not df_kospi.empty:
            for p in selected_periods:
                if len(df_kospi) > p:
                    kospi_returns[p] = (df_kospi['Close'].iloc[-1] / df_kospi['Close'].iloc[-1 - p]) - 1
                else:
                    kospi_returns[p] = 0.0

        results = []
        unique_tickers = list(set(target_list))
        
        progress_bar = st.progress(0)
        total_items = len(unique_tickers)
        
        for i, code in enumerate(unique_tickers):
            try:
                df = fdr.DataReader(code, start_date)
                if len(df) < max_p:
                    progress_bar.progress((i + 1) / total_items)
                    continue
                
                diffs = {}
                is_strong_all = True
                for p in selected_periods:
                    stock_ret = (df['Close'].iloc[-1] / df['Close'].iloc[-1 - p]) - 1
                    market_ret = kospi_returns.get(p, 0.0)
                    diff = stock_ret - market_ret
                    diffs[p] = diff
                    if stock_ret < market_ret:
                        is_strong_all = False
                
                if is_strong_all:
                    row_data = {'종목코드': code}
                    for p in selected_periods:
                        row_data[f'{p}일 초과수익'] = diffs[p]
                    sort_key = selected_periods[0]
                    row_data['Recent_Score'] = diffs[sort_key]
                    results.append(row_data)
            except Exception:
                pass
            progress_bar.progress((i + 1) / total_items)
            
        progress_bar.empty()

    if results:
        df_result = pd.DataFrame(results)
        df_result = df_result.sort_values(by='Recent_Score', ascending=False).reset_index(drop=True)
        
        display_df = df_result.drop(columns=['Recent_Score'])
        
        ret_cols = [c for c in display_df.columns if c != '종목코드']
        for col in ret_cols:
            display_df[col] = display_df[col].apply(lambda x: f"{x*100:+.2f}%")
            
        st.success(f"[{title_prefix}] 분석 완료! 총 {len(results)}개의 강세 종목이 발굴되었습니다.")
        st.dataframe(display_df, use_container_width=True)
        
        txt_header = "종목코드\t" + "\t".join([f"{p}일초과" for p in selected_periods]) + "\n"
        txt_content = txt_header
        for _, row in df_result.iterrows():
            line = f"{row['종목코드']}"
            for p in selected_periods:
                line += f"\t{row[f'{p}일 초과수익']*100:.2f}%"
            txt_content += line + "\n"
            
        st.download_button(
            label="📥 강세종목.txt 다운로드",
            data=txt_content,
            file_name="강세종목.txt",
            mime="text/plain"
        )
    else:
        st.warning("조건을 만족하는 종목이 없습니다.")

# 버튼 클릭 이벤트 분기 처리 (전체 주식+ETF)
if btn_all:
    st.info("전체 기간(10, 30, 50, 100, 200일) 주식+ETF 스크리닝을 시작합니다.")
    run_screener([10, 30, 50, 100, 200], DOMESTIC_STOCKS, "전체 주식+ETF")
elif btn_short:
    st.info("단기 집중(10일, 30일) 주식+ETF 스크리닝을 시작합니다.")
    run_screener([10, 30], DOMESTIC_STOCKS, "단기 주식+ETF")
elif btn_mid:
    st.info("중기 집중(50일, 100일) 주식+ETF 스크리닝을 시작합니다.")
    run_screener([50, 100], DOMESTIC_STOCKS, "중기 주식+ETF")
elif btn_long:
    st.info("장기 집중(200일) 주식+ETF 스크리닝을 시작합니다.")
    run_screener([200], DOMESTIC_STOCKS, "장기 주식+ETF")

# 버튼 클릭 이벤트 분기 처리 (통합 ETF 전용)
elif e_btn_all:
    st.info("전체 기간(10, 30, 50, 100, 200일) 통합 ETF 스크리닝을 시작합니다.")
    run_screener([10, 30, 50, 100, 200], ALL_ETFS, "전체 통합 ETF")
elif e_btn_short:
    st.info("단기 집중(10일, 30일) 통합 ETF 스크리닝을 시작합니다.")
    run_screener([10, 30], ALL_ETFS, "단기 통합 ETF")
elif e_btn_mid:
    st.info("중기 집중(50일, 100일) 통합 ETF 스크리닝을 시작합니다.")
    run_screener([50, 100], ALL_ETFS, "중기 통합 ETF")
elif e_btn_long:
    st.info("장기 집중(200일) 통합 ETF 스크리닝을 시작합니다.")
    run_screener([200], ALL_ETFS, "장기 통합 ETF")

# 파일별 개별 검색 버튼 이벤트 (10~200일 전체 기간 기준)
elif btn_f1:
    st.info("1. 국가별 대표지수 ETF 그룹 스크리닝을 시작합니다.")
    run_screener([10, 30, 50, 100, 200], ETF_FILE_1, "국가별 대표지수")
elif btn_f2:
    st.info("2. 혁신성장테마 ETF 그룹 스크리닝을 시작합니다.")
    run_screener([10, 30, 50, 100, 200], ETF_FILE_2, "혁신성장테마")
elif btn_f3:
    st.info("3. 국가별 섹터 ETF 그룹 스크리닝을 시작합니다.")
    run_screener([10, 30, 50, 100, 200], ETF_FILE_3, "국가별 섹터")
elif btn_f4:
    st.info("4. 안전형인컴형 ETF 그룹 스크리닝을 시작합니다.")
    run_screener([10, 30, 50, 100, 200], ETF_FILE_4, "안전형인컴형")
elif btn_f5:
    st.info("5. 원자재·부동산·통화 ETF 그룹 스크리닝을 시작합니다.")
    run_screener([10, 30, 50, 100, 200], ETF_FILE_5, "원자재·부동산·통화")
