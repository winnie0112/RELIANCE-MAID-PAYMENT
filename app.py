import datetime
import random
import streamlit as st

# 页面基本设置
st.set_page_config(
    page_title="Agensi Pekerjaan Reliance Maid - 开单系统",
    page_icon="🧾",
    layout="wide",
)

# 公司固定抬头信息
COMPANY_INFO = {
    "name": "AGENSI PEKERJAAN RELIANCE MAID SDN BHD",
    "reg_no": "(202501046992/1648400-A)",
    "address": (
        "NO 34A, JALAN BUKIT IMPIAN 16, TAMAN IMPIAN EMAS, 81300 SKUDAI, JOHOR."
    ),
    "email": "reliance.maid.agensi@gmail.com",
    "tel": "010-837 8471 / 011-2587 8401",
    "bank": "CIMB BANK ACC NO: 8606253460",
}

st.title("🧾 Reliance Maid 中介公司开单与收据系统")
st.markdown("---")

# ================= 侧边栏：输入区域 =================
st.sidebar.header("1. 客户资料 (Customer Details)")
cust_name = st.sidebar.text_input("客户姓名 (Name)", "GAN JUN HENG")
cust_ic = st.sidebar.text_input("身份证/护照号 (IC NO)", "")
cust_address = st.sidebar.text_area(
    "地址 (Address)",
    "NO 79, JALAN NAKHODA 14, TAMAN UNGKU TUN AMINAH, 81300 SKUDAI, JOHOR.",
)
cust_tel = st.sidebar.text_input("电话 (Tel)", "010-663 5030")
cust_email = st.sidebar.text_input("电子邮箱 (Email)", "")

st.sidebar.markdown("---")
st.sidebar.header("2. 业务与费用选择")

# 服务类型
service_type = st.sidebar.selectbox(
    "选择业务类型",
    [
        "Apply Maid New (新女佣申请 - 分期/全额)",
        "Permit Renewal (准证续签)",
        "Contract Renewal (合同续签)",
        "Cancel (取消)",
        "Permit (普通准证)",
        "SP (临时工作准证)",
        "Insurance (保险)",
    ],
)

maid_country = "Indonesia"
maid_name = "Sri Haryati"
payment_stage = "Invoice (完整账单)"
custom_price = 500.0

# 针对新女佣申请的特殊逻辑（包含国家、不同价钱、分期）
if service_type == "Apply Maid New (新女佣申请 - 分期/全额)":
  st.sidebar.markdown("### 🌍 女佣详情与国籍定价")
  maid_country = st.sidebar.selectbox(
      "女佣国籍 (Country)",
      ["Indonesia (印尼)", "Philippines (菲律宾)", "Vietnam (越南)"],
  )
  maid_name = st.sidebar.text_input("女佣姓名 (Maid Name)", "Sri Haryati")

  # 根据不同国家设定默认总价（你可以随时在这里修改各国的标准价）
  if "Indonesia" in maid_country:
    default_total = 17500.0
    default_deposit = 8000.0
    default_balance = 9500.0
  elif "Philippines" in maid_country:
    default_total = 19500.0
    default_deposit = 10000.0
    default_balance = 9500.0
  else:
    default_total = 16000.0
    default_deposit = 8000.0
    default_balance = 8000.0

  total_package_price = st.sidebar.number_input(
      "配套总价 (Total Package Price RM)", value=default_total
  )

  payment_stage = st.sidebar.selectbox(
      "打印单据类型",
      [
          "1. Invoice (完整总账单)",
          "2. Deposit Receipt (首付收据)",
          "3. Balance Receipt (尾款收据)",
      ],
  )
else:
  custom_price = st.sidebar.number_input(
      "费用金额 (RM)", min_value=0.0, value=500.0, step=50.0
  )

issue_date = st.sidebar.date_input(
    "单据日期 (Issue Date)", datetime.date.today()
)

# 生成单号模拟
if "inv_no" not in st.session_state:
  st.session_state.inv_no = "INV00004"

# ================= 计算并渲染模板 =================
desc_list = []
this_payment = 0.0
balance_due = 0.0
doc_title = "INVOICE"
rcpt_no = st.session_state.inv_no

if service_type == "Apply Maid New (新女佣申请 - 分期/全额)":
  rec_fee = total_package_price - 7500.0  # 拆分参考你的模板
  doc_fee = 7500.0

  if "1. Invoice" in payment_stage:
    doc_title = "INVOICE"
    rcpt_no = "INV00004"
    desc_list = [
        {
            "no": 1,
            "desc": (
                f"{maid_country.split()[0]} Maid Recruitment Fee (Maid:"
                f" {maid_name})"
            ),
            "price": rec_fee,
            "amount": rec_fee,
        },
        {
            "no": 2,
            "desc": (
                "Processing, Work Permit, Medical & Documentation Fee (Maid:"
                f" {maid_name})"
            ),
            "price": doc_fee,
            "amount": doc_fee,
        },
    ]
    this_payment = total_package_price
    balance_due = 0.00
  elif "2. Deposit Receipt" in payment_stage:
    doc_title = "RECEIPT DEPOSIT"
    rcpt_no = "RCP00004-1"
    desc_list = [{
        "no": 1,
        "desc": (
            f"Deposit Payment for Maid Recruitment ({maid_name})\n(Part"
            " payment towards total fees)"
        ),
        "price": default_deposit,
        "amount": default_deposit,
    }]
    this_payment = default_deposit
    balance_due = default_balance
  else:
    doc_title = "RECEIPT BALANCE"
    rcpt_no = "RCP00004-2"
    desc_list = [{
        "no": 1,
        "desc": (
            f"Balance Payment for Maid ({maid_name})\n(Final settlement)"
        ),
        "price": default_balance,
        "amount": default_balance,
    }]
    this_payment = default_balance
    balance_due = 0.00
else:
  doc_title = "INVOICE / RECEIPT"
  total_package_price = custom_price
  desc_list = [
      {
          "no": 1,
          "desc": f"{service_type}",
          "price": custom_price,
          "amount": custom_price,
      }
  ]
  this_payment = custom_price
  balance_due = 0.00

# ================= 网页预览区域（完美复刻你提供的 PDF 样式） =================
st.markdown("---")
st.markdown("### 📄 单据打印预览 (与你的 PDF 模板完全一致)")

st.markdown(
    f"""
<div style="border: 2px solid #333; padding: 25px; font-family: Arial, sans-serif; background-color: #fff; color: #000;">
    <!-- Company Letterhead -->
    <div style="text-align: center;">
        <h2 style="margin: 0; color: #1f3bb3;">{COMPANY_INFO['name']}</h2>
        <p style="margin: 2px; font-size: 13px; font-weight: bold;">{COMPANY_INFO['reg_no']}</p>
        <p style="margin: 2px; font-size: 12px;">{COMPANY_INFO['address']}</p>
        <p style="margin: 2px; font-size: 12px;">Email: {COMPANY_INFO['email']} | Tel: {COMPANY_INFO['tel']}</p>
    </div>
    <hr style="border: 1px solid #333; margin: 15px 0;">
    
    <!-- To & Doc Info -->
    <table style="width: 100%; font-size: 14px;">
        <tr>
            <td><strong>To:</strong><br>
                <b>{cust_name}</b><br>
                <b>IC NO:</b> {cust_ic}<br>
                {cust_address.replace(chr(10), '<br>')}<br>
                Tel: {cust_tel} | Email: {cust_email}
            </td>
            <td style="text-align: right; vertical-align: top;">
                <h3 style="margin: 0; color: #d9534f;">{doc_title}</h3>
                <p style="margin: 4px 0;"><b>INV/RCPT NO:</b> {rcpt_no}</p>
                <p style="margin: 4px 0;"><b>ISSUE DATE:</b> {issue_date}</p>
            </td>
        </tr>
    </table>
    <br>
    
    <!-- Table -->
    <table style="width: 100%; border-collapse: collapse; font-size: 14px;" border="1">
        <thead>
            <tr style="background-color: #f2f2f2;">
                <th style="padding: 8px; width: 8%; text-align: center;">NO</th>
                <th style="padding: 8px; width: 62%; text-align: left;">DESCRIPTION</th>
                <th style="padding: 8px; width: 15%; text-align: right;">PRICE (RM)</th>
                <th style="padding: 8px; width: 15%; text-align: right;">AMOUNT (RM)</th>
            </tr>
        </thead>
        <tbody>
""",
    unsafe_allow_html=True,
)

for item in desc_list:
  desc_formatted = item["desc"].replace("\n", "<br>")
  st.markdown(
      f"""
        <tr>
            <td style="padding: 8px; text-align: center;">{item['no']}</td>
            <td style="padding: 8px;">{desc_formatted}</td>
            <td style="padding: 8px; text-align: right;">{item['price']:,.2f}</td>
            <td style="padding: 8px; text-align: right;">{item['amount']:,.2f}</td>
        </tr>
    """,
      unsafe_allow_html=True,
  )

st.markdown(
    f"""
        </tbody>
    </table>
    <br>
    
    <!-- Bottom Summary -->
    <div style="float: right; width: 380px; font-size: 14px;">
        <table style="width: 100%; border-collapse: collapse;">
            {f'<tr><td style="padding: 4px;"><b>Total Package Price:</b></td><td style="text-align: right;">RM {total_package_price:,.2f}</td></tr>' if service_type.startswith('Apply Maid New') else ''}
            {f'<tr><td style="padding: 4px;"><b>Previous Paid (Deposit):</b></td><td style="text-align: right;">RM {default_deposit:,.2f}</td></tr>' if 'Receipt Balance' in payment_stage else ''}
            <tr><td style="padding: 4px;"><b>This Payment (Paid):</b></td><td style="text-align: right;"><b>RM {this_payment:,.2f}</b></td></tr>
            <tr><td style="padding: 4px; border-top: 1px solid #333;"><b>Balance Due:</b></td><td style="text-align: right; border-top: 1px solid #333;"><b>RM {balance_due:,.2f} { "(PAID IN FULL)" if balance_due == 0 and service_type.startswith('Apply Maid New') else "" }</b></td></tr>
        </table>
    </div>
    <div style="clear: both;"></div>
    
    <br>
    <p style="font-size: 13px; margin: 5px 0;"><b>Pay To / Paid To:</b><br>
    {COMPANY_INFO['name']}<br>
    <b>{COMPANY_INFO['bank']}</b></p>
    
    <div style="text-align: center; margin-top: 25px; font-weight: bold; color: #444;">
        Thank You!
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.info(
    "💡 提示：点击浏览器的 **Ctrl + P (Windows) 或 Cmd + P (Mac)**"
    " 即可直接将此页面完美排版另存为 PDF 或直接连接打印机打印出来给客户！"
)
