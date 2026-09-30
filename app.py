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
st.markdown("원하는 분석 방식을 선택하여 코스피(KOSPI) 지수 대비 아웃퍼폼한 종목을 발굴하세요.")

# 내장된 종목 리스트 (국내개별기업 200 및 TIGER/KODEX ETF)
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
    "005850", "010690", "200880", "015750", "012200", "009900", "004410", "002350", "073240",
    # TIGER & KODEX ETF 리스트
    "102110", "229200", "091230", "396500", "465640", "485520", "305540", "446770", "435550", "477570",
    "480110", "091180", "138920", "143850", "226490", "458730", "285010", "091170", "102970", "139260",
    "139270", "371460", "381180", "157490", "295820", "228790", "192090", "139280", "139290", "139240",
    "139250", "138530", "102780", "139310", "292150", "364980", "161510", "211900", "143160", "228780",
    "228800", "228810", "381420", "448290", "435570", "266420", "157450", "226480", "226500", "226510",
    "069500", "229210", "091160", "469590", "305720", "453650", "469080", "477580", "091190", "117700",
    "244580", "091120", "102710", "117460", "091220", "266390", "266370", "117690", "117680", "117420",
    "117720", "117480", "117470", "244570", "102790", "138910", "287310", "289670", "211910", "105190",
    "228750", "228770", "228760", "228820", "438410", "381430", "445220", "403560", "396510", "431290",
    "139230", "229720", "285020", "285030", "389810", "435560", "117560", "289680", "244560", "295550"
]

# 화면을 두 개의 컬럼으로 나누어 버튼 배치 (또는 세로로 배치)
col1, col2 = st.columns(2)

with col1:
    st.subheader("전체 기간 스크리닝")
    st.write("10일, 30일, 50일, 100일, 200일 **모든 기간**에서 코스피 대비 강세를 보인 종목을 찾습니다.")
    btn_all = st.button("🚀 전체 기간(5개) 강세 종목 실행", type="primary")

with col2:
    st.subheader("단기 집중 스크리닝")
    st.write("최근 트렌드 파악을 위해 **10일, 30일** 두 기간 동안만 코스피 대비 강세를 보인 종목을 찾습니다.")
    btn_short = st.button("⚡ 최근 10일·30일 단기 강세 종목 실행", type="secondary")

# 공통 실행 함수
def run_screener(selected_periods):
    max_p = max(selected_periods)
    start_date = (datetime.now() - timedelta(days=max_p + 150)).strftime('%Y-%m-%d')
    
    with st.spinner("코스피 지수 데이터 및 종목별 수익률을 분석 중입니다... 잠시만 기다려주세요."):
        df_kospi = fdr.DataReader('KS11', start_date)
        
        kospi_returns = {}
        if not df_kospi.empty:
            for p in selected_periods:
                if len(df_kospi) > p:
                    kospi_returns[p] = (df_kospi['Close'].iloc[-1] / df_kospi['Close'].iloc[-1 - p]) - 1
                else:
                    kospi_returns[p] = 0.0

        results = []
        unique_tickers = list(set(DOMESTIC_STOCKS))
        
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
                    row_data['Recent_Score'] = diffs[10] # 정렬 기준 (10일 초과수익)
                    results.append(row_data)
            except Exception:
                pass
            progress_bar.progress((i + 1) / total_items)
            
        progress_bar.empty()

    if results:
        df_result = pd.DataFrame(results)
        df_result = df_result.sort_values(by='Recent_Score', ascending=False).reset_index(drop=True)
        
        display_df = df_result.drop(columns=['Recent_Score'])
        
        # 퍼센트 포맷팅
        ret_cols = [c for c in display_df.columns if c != '종목코드']
        for col in ret_cols:
            display_df[col] = display_df[col].apply(lambda x: f"{x*100:+.2f}%")
            
        st.success(f"분석 완료! 총 {len(results)}개의 강세 종목이 발굴되었습니다.")
        st.dataframe(display_df, use_container_width=True)
        
        # 텍스트 파일 다운로드 구성
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

# 버튼 클릭 이벤트 분기 처리
if btn_all:
    st.info("전체 기간(10, 30, 50, 100, 200일) 조건으로 스크리닝을 시작합니다.")
    run_screener([10, 30, 50, 100, 200])

elif btn_short:
    st.info("단기 집중(최근 10일, 30일) 조건으로 스크리닝을 시작합니다.")
    run_screener([10, 30])
