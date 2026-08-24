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

# 侧边栏：输入区域
st.sidebar.header("1. 客户资料")
cust_name = st.sidebar.text_input("客户姓名", "GAN JUN HENG")
cust_ic = st.sidebar.text_input("身份证/护照号 (IC NO)", "")
cust_address = st.sidebar.text_area(
    "地址", "NO 79, JALAN NAKHODA 14, TAMAN UNGKU TUN AMINAH, 81300 SKUDAI, JOHOR."
)
cust_tel = st.sidebar.text_input("电话", "010-663 5030")

st.sidebar.markdown("---")
st.sidebar.header("2. 业务与费用选择")
service_type = st.sidebar.selectbox(
    "业务类型", ["Apply Maid New (新女佣申请)", "Other Service (其他服务)"]
)

maid_country = "Indonesia"
maid_name = "Sri Haryati"
payment_stage = "1. Invoice (完整总账单)"
total_package_price = 17500.0
default_deposit = 8000.0
default_balance = 9500.0

if service_type == "Apply Maid New (新女佣申请)":
  maid_country = st.sidebar.selectbox(
      "女佣国籍", ["Indonesia (印尼)", "Philippines (菲律宾)"]
  )
  maid_name = st.sidebar.text_input("女佣姓名", "Sri Haryati")

  if "Indonesia" in maid_country:
    total_package_price = 17500.0
    default_deposit = 8000.0
    default_balance = 9500.0
  else:
    total_package_price = 19500.0
    default_deposit = 10000.0
    default_balance = 9500.0

  payment_stage = st.sidebar.selectbox(
      "单据阶段",
      [
          "1. Invoice (完整总账单)",
          "2. Deposit Receipt (首付收据)",
          "3. Balance Receipt (尾款收据)",
      ],
  )
else:
  total_package_price = st.sidebar.number_input("金额 (RM)", value=500.0)

issue_date = st.sidebar.date_input("单据日期", datetime.date.today())

# 计算逻辑
this_payment = 0.0
balance_due = 0.0
doc_title = "INVOICE"
rcpt_no = "INV00004"
items = []

if service_type == "Apply Maid New (新女佣申请)":
  rec_fee = total_package_price - 7500.0
  doc_fee = 7500.0

  if "1. Invoice" in payment_stage:
    doc_title = "INVOICE"
    rcpt_no = "INV00004"
    items = [
        (
            f"{maid_country.split()[0]} Maid Recruitment Fee (Maid:"
            f" {maid_name})",
            rec_fee,
        ),
        (
            f"Processing, Work Permit, Medical & Documentation Fee (Maid:"
            f" {maid_name})",
            doc_fee,
        ),
    ]
    this_payment = total_package_price
    balance_due = 0.00
  elif "2. Deposit" in payment_stage:
    doc_title = "RECEIPT DEPOSIT"
    rcpt_no = "RCP00004-1"
    items = [(
        f"Deposit Payment for Maid Recruitment ({maid_name})",
        default_deposit,
    )]
    this_payment = default_deposit
    balance_due = default_balance
  else:
    doc_title = "RECEIPT BALANCE"
    rcpt_no = "RCP00004-2"
    items = [(f"Balance Payment for Maid ({maid_name})", default_balance)]
    this_payment = default_balance
    balance_due = 0.00
else:
  doc_title = "INVOICE / RECEIPT"
  rcpt_no = "INV00005"
  items = [(service_type, total_package_price)]
  this_payment = total_package_price
  balance_due = 0.00

# 主界面：正式单据展示
st.markdown(f"<h2 style='text-align: center;'>{COMPANY_NAME}</h2>", unsafe_allow_html=True)
st.markdown(
    f"<p style='text-align: center; font-size: 14px; font-weight: bold;'>{COMPANY_REG}</p>",
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

col1, col2 = st.columns([1.2, 0.8])

with col1:
  st.markdown("**To:**")
  st.markdown(f"**{cust_name}**")
  if cust_ic:
    st.markdown(f"**IC NO:** {cust_ic}")
  st.markdown(f"{cust_address}")
  st.markdown(f"Tel: {cust_tel}")

with col2:
  st.markdown(f"### <span style='color:red;'>{doc_title}</span>", unsafe_allow_html=True)
  st.markdown(f"**No:** {rcpt_no}")
  st.markdown(f"**Date:** {issue_date}")

st.markdown("---")

# 表格数据展示
st.markdown("#### 费用明细 (Description)")
for i, (desc, amt) in enumerate(items, 1):
  c_a, c_b, c_c = st.columns([0.1, 0.6, 0.3])
  c_a.write(str(i))
  c_b.write(desc)
  c_c.write(f"RM {amt:,.2f}")

st.markdown("---")

# 总结算区域
st.markdown("#### 结算总额")
if service_type.startswith("Apply Maid New"):
  st.write(f"**Total Package Price:** RM {total_package_price:,.2f}")
  if "Balance" in payment_stage:
    st.write(f"**Previous Paid (Deposit):** RM {default_deposit:,.2f}")

st.success(f"**This Payment (Paid): RM {this_payment:,.2f}**")
if service_type.startswith("Apply Maid New"):
  st.info(
      f"**Balance Due (尾款): RM {balance_due:,.2f}**"
      f" {'(PAID IN FULL)' if balance_due == 0 else ''}"
  )

st.markdown("---")
st.markdown(f"**Pay To / Paid To:**\n\n{COMPANY_NAME}\n\n**{COMPANY_BANK}**")
st.markdown(
    "<h4 style='text-align: center; color: gray;'>Thank You!</h4>",
    unsafe_allow_html=True,
)
