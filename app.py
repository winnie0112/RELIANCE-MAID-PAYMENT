import datetime
import streamlit as st

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

# 侧边栏输入
st.sidebar.header("1. 客户资料")
cust_name = st.sidebar.text_input("客户姓名", "GAN JUN HENG")
cust_ic = st.sidebar.text_input("身份证/护照号 (IC NO)", "")
cust_address = st.sidebar.text_area(
    "地址", "NO 79, JALAN NAKHODA 14, TAMAN UNGKU TUN AMINAH, 81300 SKUDAI, JOHOR."
)
cust_tel = st.sidebar.text_input("电话", "010-663 5030")

st.sidebar.markdown("---")
st.sidebar.header("2. 女佣与费用选择")
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

# 数据处理
desc_list = []
this_payment = 0.0
balance_due = 0.0
doc_title = "INVOICE"
rcpt_no = "INV00004"

if service_type == "Apply Maid New (新女佣申请)":
  rec_fee = total_package_price - 7500.0
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
  elif "2. Deposit" in payment_stage:
    doc_title = "RECEIPT DEPOSIT"
    rcpt_no = "RCP00004-1"
    desc_list = [{
        "no": 1,
        "desc": (
            f"Deposit Payment for Maid Recruitment ({maid_name})<br><small>(Part"
            " payment towards total fees)</small>"
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
            f"Balance Payment for Maid ({maid_name})<br><small>(Final"
            " settlement)</small>"
        ),
        "price": default_balance,
        "amount": default_balance,
    }]
    this_payment = default_balance
    balance_due = 0.00
else:
  doc_title = "INVOICE / RECEIPT"
  rcpt_no = "INV00005"
  desc_list = [{
      "no": 1,
      "desc": service_type,
      "price": total_package_price,
      "amount": total_package_price,
  }]
  this_payment = total_package_price
  balance_due = 0.00

# 拼装 HTML
rows_html = ""
for item in desc_list:
  rows_html += f"""
    <tr>
        <td style="padding: 8px; text-align: center;">{item['no']}</td>
        <td style="padding: 8px;">{item['desc']}</td>
        <td style="padding: 8px; text-align: right;">{item['price']:,.2f}</td>
        <td style="padding: 8px; text-align: right;">{item['amount']:,.2f}</td>
    </tr>
    """

summary_html = f"""
    <table style="width: 100%; border-collapse: collapse;">
        {'<tr><td style="padding: 4px;"><b>Total Package Price:</b></td><td style="text-align: right;">RM ' + f'{total_package_price:,.2f}' + '</td></tr>' if service_type.startswith('Apply Maid New') else ''}
        {'<tr><td style="padding: 4px;"><b>Previous Paid (Deposit):</b></td><td style="text-align: right;">RM ' + f'{default_deposit:,.2f}' + '</td></tr>' if 'Balance' in payment_stage else ''}
        <tr><td style="padding: 4px;"><b>This Payment (Paid):</b></td><td style="text-align: right;"><b>RM {this_payment:,.2f}</b></td></tr>
        <tr><td style="padding: 4px; border-top: 1px solid #333;"><b>Balance Due:</b></td><td style="text-align: right; border-top: 1px solid #333;"><b>RM {balance_due:,.2f} {"(PAID IN FULL)" if balance_due == 0 and service_type.startswith("Apply Maid New") else ""}</b></td></tr>
    </table>
"""

html_content = f"""
<div style="border: 2px solid #333; padding: 25px; font-family: Arial, sans-serif; background-color: #fff; color: #000;">
    <div style="text-align: center;">
        <h2 style="margin: 0; color: #1f3bb3;">{COMPANY_INFO['name']}</h2>
        <p style="margin: 2px; font-size: 13px; font-weight: bold;">{COMPANY_INFO['reg_no']}</p>
        <p style="margin: 2px; font-size: 12px;">{COMPANY_INFO['address']}</p>
        <p style="margin: 2px; font-size: 12px;">Email: {COMPANY_INFO['email']} | Tel: {COMPANY_INFO['tel']}</p>
    </div>
    <hr style="border: 1px solid #333; margin: 15px 0;">
    
    <table style="width: 100%; font-size: 14px; border:none;">
        <tr style="border:none;">
            <td style="border:none;"><strong>To:</strong><br>
                <b>{cust_name}</b><br>
                <b>IC NO:</b> {cust_ic}<br>
                {cust_address}<br>
                Tel: {cust_tel}
            </td>
            <td style="text-align: right; vertical-align: top; border:none;">
                <h3 style="margin: 0; color: #d9534f;">{doc_title}</h3>
                <p style="margin: 4px 0;"><b>INV/RCPT NO:</b> {rcpt_no}</p>
                <p style="margin: 4px 0;"><b>ISSUE DATE:</b> {issue_date}</p>
            </td>
        </tr>
    </table>
    <br>
    
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
            {rows_html}
        </tbody>
    </table>
    <br>
    
    <div style="float: right; width: 380px; font-size: 14px;">
        {summary_html}
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
"""

st.markdown(html_content, unsafe_allow_html=True)
