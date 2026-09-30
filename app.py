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

st.title("📈 국내 및 미국 주식·ETF 상대 강세(Relative Strength) 스크리너 📈")
st.markdown("원하는 대상과 분석 기간을 선택하여 코스피, S&P 500, 나스닥 100 지수 대비 아웃퍼폼한 종목을 발굴하세요.")

# 1. 국내 전체 종목 리스트
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

# 2. ETF 파일별 리스트
ETF_FILE_1 = [
    "192090", "245360", "117690", "365040", "228820", "232080", "277650", "277640", "277630", "252000", 
    "292160", "292150", "289480", "310960", "310970", "102110", "166400", "289260", "289250", "0204S0", 
    "461580", "496080", "105010", "453870", "133690", "245340", "360750", "143850", "0238P0", "418660", 
    "429010", "435420", "0223R0", "488500", "448290", "448300", "441680", "241180", "195920", "195930"
]
ETF_FILE_2 = [
    "0190Y0", "0241R0", "381180", "396500", "396520", "480310", "453950", "0233J0", "466950", "0177R0", 
    "471760", "0053L0", "0117V0", "0148J0", "491010", "0067Y0", "0102A0", "465660", "449690", "491830", 
    "497570", "0142D0", "0123G0", "376410", "396510", "377990", "417630", "404540", "0091P0", "365000", 
    "364990", "400970", "371450", "412770", "300610", "418670", "364980", "394670", "387280", "394660", 
    "371460", "305540", "462010", "0067V0", "447770", "449680", "371470", "364970", "476690", "0168K0", 
    "371160", "364960", "387270", "275980", "381170", "414780", "493810", "472160", "472170", "0047A0", 
    "463250", "464930", "464310", "490090"
]
ETF_FILE_3 = [
    "203780", "0183J0", "458730", "0015K0", "494840", "248270", "479730", "269370", "276000", "0060H0", 
    "0133E0", "139270", "091220", "139230", "139280", "143860", "157490", "139250", "157500", "091230", 
    "227540", "227550", "228800", "237440", "210780", "261060", "228810", "315270", "307510", "307520", 
    "138540", "147970", "227560", "261140", "138520", "138530", "139220", "139240", "228790", "211560", 
    "150460", "139260", "261070", "494670", "174350", "139290", "227570"
]
ETF_FILE_4 = [
    "289480", "166400", "482730", "458750", "486290", "0104N0", "0104P0", "493810", "0000D0", "474220", 
    "441680", "0008S0", "458760", "245350", "429000", "0052D0", "472150", "466940", "445910", "465670", 
    "357870", "499660", "440340", "456610", "475630", "449170", "480260", "0094K0", "0192Z0", "157450", 
    "272580", "305080", "329750", "438330", "302190", "182490", "114820", "451530", "0043B0", "0046A0", 
    "0139F0", "476550", "458250", "458260", "451540", "237440", "0025N0", "447770"
]
ETF_FILE_5 = [
    "139320", "0189B0", "319640", "137610", "160580", "130680", "0072R0", "292560", "182480", "329200", 
    "341850", "0086B0", "0086C0"
]
ALL_ETFS = list(set(ETF_FILE_1 + ETF_FILE_2 + ETF_FILE_3 + ETF_FILE_4 + ETF_FILE_5))

# 3. 미국 상위 100대 기업 티커 리스트
US_TOP_100 = [
    "NVDA", "AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "META", "AVGO", "TSLA", "MU", 
    "LLY", "JPM", "WMT", "AMD", "BRK.B", "V", "XOM", "JNJ", "INTC", "MA", 
    "ABBV", "CSCO", "ORCL", "CVX", "PLTR", "BAC", "COST", "KO", "CAT", "DELL", 
    "MRK", "PG", "LRCX", "UNH", "AMAT", "GE", "MS", "NFLX", "PANW", "HD", 
    "PM", "GS", "WFC", "RTX", "ANET", "CRWD", "GEV", "TXN", "TMO", "IBM", 
    "C", "SNDK", "KLAC", "AXP", "VZ", "MRVL", "CRM", "AMGN", "QCOM", "APH", 
    "PEP", "PFE", "ABT", "MCD", "DIS", "INTU", "NOW", "CMCSA", "TMUS", "BKNG", 
    "SBUX", "GILD", "NKE", "BLK", "CCEP", "UNP", "LOW", "COP", "VRTX", "ADBE", 
    "SHOP", "PYPL", "DDOG", "ABNB", "DASH", "APP", "CEG", "LIN", "ADI", "HON", 
    "WDC", "STX", "MDT", "SNOW", "WDAY", "SNPS", "CDNS", "REGN", "MDLZ", "ISRG", "MCHP"
] # 미국상위100대기업[cite: 13]


# --- UI 레이아웃 구성 ---

st.subheader("📊 전체 국내 종목 (주식 + ETF) 스크리너")
col1, col2, col3, col4 = st.columns(4)
with col1: btn_all = st.button("🚀 전체기간 (주식+ETF)", type="primary")
with col2: btn_short = st.button("⚡ 단기 10·30일 (주식+ETF)")
with col3: btn_mid = st.button("🔍 중기 50·100일 (주식+ETF)")
with col4: btn_long = st.button("🐢 장기 200일 (주식+ETF)")

st.markdown("---")

# 미국 상위 100대 기업 스크리너 세션 (S&P 500 및 나스닥 100 기준)
st.subheader("📊🇺🇸 미국 상위 100대 기업 상대 강세 스크리너")

st.markdown("**[S&P 500 지수 대비 강세 종목]**")
us1_all, us1_short, us1_mid, us1_long = st.columns(4)
with us1_all: us_sp_all = st.button("🚀 전체기간 (vs S&P500)", key="us_sp_all")
with us1_short: us_sp_short = st.button("⚡ 10·30일 (vs S&P500)", key="us_sp_short")
with us1_mid: us_sp_mid = st.button("🔍 50·100일 (vs S&P500)", key="us_sp_mid")
with us1_long: us_sp_long = st.button("🐢 200일 (vs S&P500)", key="us_sp_long")

st.markdown("")
st.markdown("**[나스닥 100 지수 대비 강세 종목]**")
us2_all, us2_short, us2_mid, us2_long = st.columns(4)
with us2_all: us_nd_all = st.button("🚀 전체기간 (vs Nasdaq100)", key="us_nd_all")
with us2_short: us_nd_short = st.button("⚡ 10·30일 (vs Nasdaq100)", key="us_nd_short")
with us2_mid: us_nd_mid = st.button("🔍 50·100일 (vs Nasdaq100)", key="us_nd_mid")
with us2_long: us_nd_long = st.button("🐢 200일 (vs Nasdaq100)", key="us_nd_long")

st.markdown("---")

st.subheader("🎯 전체 ETF 통합 전용 스크리너")
ecol1, ecol2, ecol3, ecol4 = st.columns(4)
with ecol1: e_btn_all = st.button("🚀 전체기간 (통합ETF)")
with ecol2: e_btn_short = st.button("⚡ 단기 10·30일 (통합ETF)")
with ecol3: e_btn_mid = st.button("🔍 중기 50·100일 (통합ETF)")
with ecol4: e_btn_long = st.button("🐢 장기 200일 (통합ETF)")

st.markdown("---")

st.subheader("📂 파일별 개별 ETF 그룹 스크리너")
def render_file_section(title, file_key):
    st.markdown(f"**[{title}]**")
    b1, b2, b3, b4 = st.columns(4)
    with b1: bt_all = st.button("🚀 전체기간", key=f"{file_key}_all")
    with b2: bt_short = st.button("⚡ 10·30일", key=f"{file_key}_short")
    with b3: bt_mid = st.button("🔍 50·100일", key=f"{file_key}_mid")
    with b4: bt_long = st.button("🐢 200일", key=f"{file_key}_long")
    st.markdown("")
    return bt_all, bt_short, bt_mid, bt_long

f1_all, f1_short, f1_mid, f1_long = render_file_section("1. 국가별 대표지수", "f1")
f2_all, f2_short, f2_mid, f2_long = render_file_section("2. 혁신성장테마", "f2")
f3_all, f3_short, f3_mid, f3_long = render_file_section("3. 국가별 섹터", "f3")
f4_all, f4_short, f4_mid, f4_long = render_file_section("4. 안전형인컴형", "f4")
f5_all, f5_short, f5_mid, f5_long = render_file_section("5. 원자재·부동산·통화", "f5")


# 공통 실행 함수
def run_screener(selected_periods, target_list, title_prefix, market_ticker='KS11'):
    max_p = max(selected_periods)
    start_date = (datetime.now() - timedelta(days=max_p + 150)).strftime('%Y-%m-%d')
    
    with st.spinner(f"벤치마크({market_ticker}) 데이터 및 [{title_prefix}] 수익률을 분석 중입니다... 잠시만 기다려주세요."):
        try:
            df_market = fdr.DataReader(market_ticker, start_date)
        except Exception:
            st.error(f"벤치마크 지수({market_ticker}) 데이터를 가져오는 데 실패했습니다.")
            return
        
        market_returns = {}
        if not df_market.empty:
            for p in selected_periods:
                if len(df_market) > p:
                    market_returns[p] = (df_market['Close'].iloc[-1] / df_market['Close'].iloc[-1 - p]) - 1
                else:
                    market_returns[p] = 0.0

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
                    market_ret = market_returns.get(p, 0.0)
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


# --- 버튼 클릭 이벤트 분기 처리 ---

# 국내 주식+ETF
if btn_all: run_screener([10, 30, 50, 100, 200], DOMESTIC_STOCKS, "전체 주식+ETF (전체기간)", 'KS11')
elif btn_short: run_screener([10, 30], DOMESTIC_STOCKS, "전체 주식+ETF (단기)", 'KS11')
elif btn_mid: run_screener([50, 100], DOMESTIC_STOCKS, "전체 주식+ETF (중기)", 'KS11')
elif btn_long: run_screener([200], DOMESTIC_STOCKS, "전체 주식+ETF (장기)", 'KS11')

# 미국 상위 100대 기업 (S&P 500 대비: 'S&P500')
elif us_sp_all: run_screener([10, 30, 50, 100, 200], US_TOP_100, "미국 상위 100 (vs S&P 500 전체기간)", 'S&P500')
elif us_sp_short: run_screener([10, 30], US_TOP_100, "미국 상위 100 (vs S&P 500 단기)", 'S&P500')
elif us_sp_mid: run_screener([50, 100], US_TOP_100, "미국 상위 100 (vs S&P 500 중기)", 'S&P500')
elif us_sp_long: run_screener([200], US_TOP_100, "미국 상위 100 (vs S&P 500 장기)", 'S&P500')

# 미국 상위 100대 기업 (나스닥 100 대비: '^NDX')
elif us_nd_all: run_screener([10, 30, 50, 100, 200], US_TOP_100, "미국 상위 100 (vs Nasdaq 100 전체기간)", '^NDX')
elif us_nd_short: run_screener([10, 30], US_TOP_100, "미국 상위 100 (vs Nasdaq 100 단기)", '^NDX')
elif us_nd_mid: run_screener([50, 100], US_TOP_100, "미국 상위 100 (vs Nasdaq 100 중기)", '^NDX')
elif us_nd_long: run_screener([200], US_TOP_100, "미국 상위 100 (vs Nasdaq 100 장기)", '^NDX')

# 통합 ETF 전용
elif e_btn_all: run_screener([10, 30, 50, 100, 200], ALL_ETFS, "통합 ETF (전체기간)", 'KS11')
elif e_btn_short: run_screener([10, 30], ALL_ETFS, "통합 ETF (단기)", 'KS11')
elif e_btn_mid: run_screener([50, 100], ALL_ETFS, "통합 ETF (중기)", 'KS11')
elif e_btn_long: run_screener([200], ALL_ETFS, "통합 ETF (장기)", 'KS11')

# 파일 1~5 그룹
elif f1_all: run_screener([10, 30, 50, 100, 200], ETF_FILE_1, "국가별 대표지수 (전체기간)", 'KS11')
elif f1_short: run_screener([10, 30], ETF_FILE_1, "국가별 대표지수 (단기)", 'KS11')
elif f1_mid: run_screener([50, 100], ETF_FILE_1, "국가별 대표지수 (중기)", 'KS11')
elif f1_long: run_screener([200], ETF_FILE_1, "국가별 대표지수 (장기)", 'KS11')

elif f2_all: run_screener([10, 30, 50, 100, 200], ETF_FILE_2, "혁신성장테마 (전체기간)", 'KS11')
elif f2_short: run_screener([10, 30], ETF_FILE_2, "혁신성장테마 (단기)", 'KS11')
elif f2_mid: run_screener([50, 100], ETF_FILE_2, "혁신성장테마 (중기)", 'KS11')
elif f2_long: run_screener([200], ETF_FILE_2, "혁신성장테마 (장기)", 'KS11')

elif f3_all: run_screener([10, 30, 50, 100, 200], ETF_FILE_3, "국가별 섹터 (전체기간)", 'KS11')
elif f3_short: run_screener([10, 30], ETF_FILE_3, "국가별 섹터 (단기)", 'KS11')
elif f3_mid: run_screener([50, 100], ETF_FILE_3, "국가별 섹터 (중기)", 'KS11')
elif f3_long: run_screener([200], ETF_FILE_3, "국가별 섹터 (장기)", 'KS11')

elif f4_all: run_screener([10, 30, 50, 100, 200], ETF_FILE_4, "안전형인컴형 (전체기간)", 'KS11')
elif f4_short: run_screener([10, 30], ETF_FILE_4, "안전형인컴형 (단기)", 'KS11')
elif f4_mid: run_screener([50, 100], ETF_FILE_4, "안전형인컴형 (중기)", 'KS11')
elif f4_long: run_screener([200], ETF_FILE_4, "안전형인컴형 (장기)", 'KS11')

elif f5_all: run_screener([10, 30, 50, 100, 200], ETF_FILE_5, "원자재·부동산·통화 (전체기간)", 'KS11')
elif f5_short: run_screener([10, 30], ETF_FILE_5, "원자재·부동산·통화 (단기)", 'KS11')
elif f5_mid: run_screener([50, 100], ETF_FILE_5, "원자재·부동산·통화 (중기)", 'KS11')
elif f5_long: run_screener([200], ETF_FILE_5, "원자재·부동산·통화 (장기)", 'KS11')
