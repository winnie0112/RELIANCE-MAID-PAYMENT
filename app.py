import datetime
import streamlit as st

st.set_page_config(
    page_title="Agensi Pekerjaan Reliance Maid - 开单系统",
    page_icon="🧾",
    layout="centered",
)

# 公司固定抬头信息
COMPANY_NAME = "AGENSI PEKERJAAN RELIANCE MAID SDN BHD"
COMPANY_REG = "(202501046992/1648400-A)"
COMPANY_ADDR = (
    "NO 34A, JALAN BUKIT IMPIAN 16, TAMAN IMPIAN EMAS, 81300 SKUDAI, JOHOR."
)
COMPANY_CONTACT = (
    "Email: reliance.maid.agensi@gmail.com | Tel: 010-837 8471 / 011-2587 8401"
)
COMPANY_BANK = "CIMB BANK ACC NO: 8606253460"

# 侧边栏：客户与单据设定
st.sidebar.header("1. 客户资料")
cust_name = st.sidebar.text_input("客户姓名", "GAN JUN HENG")
cust_ic = st.sidebar.text_input("身份证/护照号 (IC NO)", "900101-01-1234")
cust_address = st.sidebar.text_area(
    "地址", "NO 79, JALAN NAKHODA 14, TAMAN UNGKU TUN AMINAH, 81300 SKUDAI, JOHOR."
)
cust_tel = st.sidebar.text_input("电话", "010-663 5030")

st.sidebar.markdown("---")
st.sidebar.header("2. 单据与费用设定")
doc_title = st.sidebar.selectbox(
    "单据类型",
    [
        "INVOICE",
        "RECEIPT DEPOSIT",
        "RECEIPT BALANCE",
        "INVOICE / RECEIPT",
    ],
)
rcpt_no = st.sidebar.text_input("单据编号 (No)", "INV00004")
issue_date = st.sidebar.date_input("单据日期", datetime.date.today())

st.sidebar.markdown("---")
st.sidebar.header("3. 自定义收费项目")
num_items = st.sidebar.number_input("项目行数", min_value=1, max_value=5, value=2)
items = []
total_amount = 0.0

for i in range(int(num_items)):
  st.sidebar.subheader(f"项目 {i+1}")
  desc = st.sidebar.text_input(
      f"内容描述 {i+1}",
      (
          "Indonesia Maid Recruitment Fee"
          if i == 0
          else "Processing & Work Permit Fee"
      ),
      key=f"desc_{i}",
  )
  price = st.sidebar.number_input(
      f"金额 RM {i+1}", value=8750.0 if i == 0 else 7500.0, key=f"price_{i}"
  )
  items.append({"no": i + 1, "desc": desc, "amount": price})
  total_amount += price

# --- 主界面：完全使用原生组件展示，绝不出现 HTML 代码 ---
st.markdown(
    f"<h2 style='text-align: center; color: #1f3bb3;'>{COMPANY_NAME}</h2>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<p style='text-align: center; font-size: 13px; font-weight:"
    f" bold;'>{COMPANY_REG}</p>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<p style='text-align: center; font-size: 12px;'>{COMPANY_ADDR}</p>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<p style='text-align: center; font-size: 12px;'>{COMPANY_CONTACT}</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# 客户与单据信息分栏
col1, col2 = st.columns([1.2, 0.8])
with col1:
  st.markdown("**To:**")
  st.markdown(f"**{cust_name}**")
  if cust_ic:
    st.markdown(f"**IC NO:** {cust_ic}")
  st.markdown(f"{cust_address}")
  st.markdown(f"Tel: {cust_tel}")

with col2:
  st.markdown(f"### 🔴 {doc_title}")
  st.markdown(f"**No:** {rcpt_no}")
  st.markdown(f"**Date:** {issue_date}")

st.markdown("---")

# 费用明细标题
st.markdown("#### 📋 费用明细 (Description)")

# 用美观的列表展示项目，绝对安全不出代码
for item in items:
  c_a, c_b, c_c = st.columns([0.1, 0.7, 0.2])
  c_a.write(f"**{item['no']}.**")
  c_b.write(item["desc"])
  c_c.write(f"**RM {item['amount']:,.2f}**")
  st.markdown("<hr style='margin: 5px 0; border: 0.5px solid #eee;'>", unsafe_allow_html=True)

# 总金额
st.markdown("---")
st.success(f"### 总计 (Total): RM {total_amount:,.2f}")

# 银行信息与落款
st.markdown("---")
st.markdown(f"**Pay To / Paid To:**\n\n{COMPANY_NAME}\n\n**{COMPANY_BANK}**")
st.markdown(
    "<h4 style='text-align: center; color: gray;'>Thank You!</h4>",
    unsafe_allow_html=True,
)

# 保存 PDF 提示
st.markdown("---")
st.info(
    "💡 **如何保存为 PDF？**\n\n"
    "您只需点击手机浏览器右上角的菜单（三个点 **`...`**），选择 **`分享`** 或 **`打印`**，"
    "然后在打印选项里选择 **`另存为 PDF`**（Save as PDF），即可秒速生成并下载完美的 PDF 收据！"
)
