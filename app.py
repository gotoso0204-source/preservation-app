import datetime
import json
import os
import streamlit as st

# 1. ページ全体の初期設定
st.set_page_config(
    page_title="DX Equipment Hub",
    page_icon="⚡",
    layout="wide",
)

# 2. モダンデザインのカスタムCSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b0e14;
        color: #e6edf3;
    }
    
    .portal-header {
        background: linear-gradient(135deg, #1f293d 0%, #111827 100%);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #1f2937;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    
    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38ef7d 0%, #11998e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .hero-subtitle {
        color: #9ca3af;
        font-size: 0.9rem;
        margin-top: 4px;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #111827;
        border-radius: 14px !important;
        border: 1px solid #1f2937 !important;
    }

    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        border: none;
    }

    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        border-radius: 8px;
        background-color: #0b0e14;
        color: #ffffff;
        border: 1px solid #1f2937;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. データの読み書き関数（JSONファイル保存）
DATA_FILE = "reservations.json"


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# セッション状態の初期化（ファイルから読み込む）
if "reservations" not in st.session_state:
    st.session_state.reservations = load_data()


# データの変更時に自動保存するヘルパー関数
def update_and_save(new_reservations):
    st.session_state.reservations = new_reservations
    save_data(new_reservations)


# ヘッダーエリア
st.markdown(
    """
    <div class="portal-header">
        <p class="hero-title">⚡ DX LAB RESERVATION</p>
        <p class="hero-subtitle">機材予約・成果物シェア ポータル（永続保存対応）</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# 名簿データ
STUDENT_ROSTER = [
    "-- 氏名を選択してください --",
    "小笹",
    "津田",
    "安見",
    "山崎",
    "松岡",
    "平林",
    "砂山",
    "川本",
    "加藤",
    "岩田",
    "入江",
    "中村",
    "内田",
    "岡田",
    "橋爪",
    "奥野",
    "南",
    "西出",
    "後藤",
    "竹市",
    "岡本",
    "飯島",
    "永田",
]

EQUIPMENT_LIST = [
    "3Dプリンター #1",
    "3Dプリンター #2",
    "VRヘッドセット A",
    "VRヘッドセット B",
    "高性能動画編集PC",
]

tab1, tab2 = st.tabs(["📅 タイムテーブル予約", "🎨 成果物ギャラリー (イイネ・コメント)"])

with tab1:
    c1, c2 = st.columns([1, 1])
    with c1:
        selected_equipment = st.selectbox("📦 機材を選択", EQUIPMENT_LIST)
    with c2:
        today = datetime.date.today()
        selected_date = st.date_input("📅 利用日を選択", value=today, min_value=today)
        date_str = selected_date.strftime("%Y-%m-%d")

    time_slots = [
        "09:00 - 09:30", "09:30 - 10:00", "10:00 - 10:30", "10:30 - 11:00",
        "11:00 - 11:30", "11:30 - 12:00", "13:00 - 13:30", "13:30 - 14:00",
        "14:00 - 14:30", "14:30 - 15:00", "15:00 - 15:30", "15:30 - 16:00",
        "16:00 - 16:30", "16:30 - 17:00", "17:00 - 17:30", "17:30 - 18:00",
        "18:00 - 18:30", "18:30 - 19:00"
    ]

    st.markdown("---")
    st.subheader(f"📌 {selected_equipment} の予約状況 ({date_str})")

    cols = st.columns(3)

    for i, slot in enumerate(time_slots):
        key = f"{selected_equipment}_{date_str}_{slot}"
        res_info = st.session_state.reservations.get(key)

        with cols[i % 3]:
            with st.container(border=True):
                if res_info is None:
                    st.markdown(f"### {slot}")
                    st.caption("🟢 空き")
                    
                    selected_student = st.selectbox("予約者氏名 (名簿)", STUDENT_ROSTER, key=f"name_{key}")
                    
                    if st.button("予約を確定する", key=f"btn_{key}", use_container_width=True, type="primary"):
                        if selected_student != STUDENT_ROSTER[0]:
                            current_data = st.session_state.reservations
                            current_data[key] = {
                                "user": selected_student,
                                "status": "利用中",
                                "artifact_text": "",
                                "artifact_image": None,
                                "likes": 0,
                                "comments": []
                            }
                            update_and_save(current_data)
                            st.toast(f"🎉 {slot} の予約を開始しました！", icon="✅")
                            st.rerun()
                        else:
                            st.error("名簿から自分の名前を選択してください。")
                else:
                    status = res_info["status"]
                    user = res_info["user"]

                    st.markdown(f"### {slot}")
                    st.markdown(f"使用者: **{user}**")
                    
                    if status != "完了":
                        st.caption("🟡 利用中 / 成果物を作成中")
                        
                        art_text = st.text_area("作業メモ・感想", value=res_info.get("artifact_text", ""), key=f"text_{key}", placeholder="例: 3Dプリンターで出力成功！")
                        # 画像ファイルはJSONに直接保存できないためテキスト中心の共有になります
                        
                        current_data = st.session_state.reservations
                        current_data[key]["artifact_text"] = art_text
                        update_and_save(current_data)

                        col_act1, col_act2 = st.columns(2)
                        with col_act1:
                            if st.button("🏁 完了して公開", key=f"end_{key}", use_container_width=True, type="primary"):
                                current_data[key]["status"] = "完了"
                                update_and_save(current_data)
                                st.toast("🙌 ギャラリーに公開しました！")
                                st.rerun()
                        with col_act2:
                            if st.button("❌ 取消", key=f"cancel_{key}", use_container_width=True):
                                current_data = st.session_state.reservations
                                del current_data[key]
                                update_and_save(current_data)
                                st.toast("予約をキャンセルしました。")
                                st.rerun()
                    else:
                        st.caption("🔵 公開済み")
                        if st.button("🔄 編集・リセット", key=f"reset_{key}", use_container_width=True):
                            current_data = st.session_state.reservations
                            del current_data[key]
                            update_and_save(current_data)
                            st.rerun()

with tab2:
    st.subheader("🎨 みんなの成果物ギャラリー")
    
    all_items = list(st.session_state.reservations.items())

    if all_items:
        for k, v in all_items:
            eq, d, sl = k.split("_", 2)
            with st.container(border=True):
                col_info, col_like = st.columns([4, 1])
                
                with col_info:
                    st.markdown(f"**📦 機材:** {eq} ／ **日時:** {d} {sl}")
                    st.markdown(f"👤 作成者: **{v['user']}**")
                    
                    if v.get("artifact_text"):
                        st.info(f"💬 メモ: {v['artifact_text']}")
                    else:
                        st.write("*(作業メモはまだありません)*")
                
                with col_like:
                    st.markdown("<br>", unsafe_allow_html=True)
                    likes_count = v.get("likes", 0)
                    if st.button(f"❤️ {likes_count}", key=f"gallery_like_{k}", use_container_width=True):
                        current_data = st.session_state.reservations
                        current_data[k]["likes"] = likes_count + 1
                        update_and_save(current_data)
                        st.rerun()
                
                st.markdown("---")
                st.markdown("💬 **コメントセクション**")
                
                comments = v.get("comments", [])
                if comments:
                    for comm in comments:
                        st.markdown(f"- **{comm['author']}**: {comm['text']}")
                else:
                    st.caption("まだコメントはありません。最初のコメントを書いてみよう！")
                
                c_col1, c_col2, c_col3 = st.columns([2, 3, 1])
                with c_col1:
                    c_name = st.selectbox("名前 (名簿)", STUDENT_ROSTER, key=f"g_name_{k}")
                with c_col2:
                    c_text = st.text_input("コメント", key=f"g_text_{k}", placeholder="すごいですね！")
                with c_col3:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("送信", key=f"g_btn_{k}", use_container_width=True):
                        if c_name != STUDENT_ROSTER[0] and c_text.strip():
                            current_data = st.session_state.reservations
                            current_data[k]["comments"].append({
                                "author": c_name,
                                "text": c_text.strip()
                            })
                            update_and_save(current_data)
                            st.toast("💬 コメントを送信しました！")
                            st.rerun()
                        else:
                            st.warning("名前（名簿から選択）とコメントを入力してください。")
    else:
        st.info("まだ予約や投稿がありません。「タイムテーブル予約」タブから枠を確保してみましょう！")
