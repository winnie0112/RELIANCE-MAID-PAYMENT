import datetime
import random
import pandas as pd
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

st.title("🧾 女佣中介公司开单与收据管理系统")
st.markdown("---")

# ================= 侧边栏：输入区域 =================
st.sidebar.header("1. 客户资料 (Customer Details)")
cust_name = st.sidebar.text_input("客户姓名 (Name)", "GAN JUN HENG")
cust_ic = st.sidebar.text_input("身份证/护照号 (IC/Passport)", "")
cust_address = st.sidebar.text_area(
    "地址 (Address)",
    "NO 79, JALAN NAKHODA 14, TAMAN UNGKU TUN AMINAH, 81300 SKUDAI, JOHOR.",
)
cust_tel = st.sidebar.text_input("电话 (Tel)", "010-663 5030")
cust_email = st.sidebar.text_input("电子邮箱 (Email)", "")

st.sidebar.markdown("---")
st.sidebar.header("2. 业务与费用选择 (Service & Fees)")

# 业务选项
service_type = st.sidebar.selectbox(
    "选择服务项目",
    [
        "Apply Maid New (新女佣申请)",
        "Permit Renewal (准证续签)",
        "Contract Renewal (合同续签)",
        "Cancel (取消)",
        "Permit (普通准证)",
        "SP (临时工作准证)",
        "Insurance (保险)",
    ],
)

maid_name = ""
payment_stage = "一次性付清 (Full Payment)"

# 针对 Apply Maid New 的特殊逻辑
if service_type == "Apply Maid New (新女佣申请)":
  maid_name = st.sidebar.text_input("女佣姓名 (Maid Name)", "Sri Haryati")
  payment_stage = st.sidebar.radio(
      "付款阶段 (Payment Stage)",
      ["Deposit (首付 RM 8,000)", "Balance (尾款 RM 9,500)", "Full Paid (全额)"],
  )
else:
  # 其他服务让用户自定义价格
  custom_price = st.sidebar.number_input(
      "费用金额 (RM)", min_value=0.0, value=500.0, step=50.0
  )

issue_date = st.sidebar.date_input(
    "单据日期 (Issue Date)", datetime.date.today()
)

# ================= 主界面：生成单据预览 =================
# 自动生成单号模拟
if "inv_no" not in st.session_state:
  st.session_state.inv_no = f"INV{random.randint(10000, 99999)}"

col1, col2 = st.columns([2, 1])
with col2:
  if st.button("🔄 重新生成单号"):
    st.session_state.inv_no = f"INV{random.randint(10000, 99999)}"

# 开始计算价格与生成单据内容
desc_list = []
total_package_price = 0.0
this_payment = 0.0
balance_due = 0.0
doc_title = "INVOICE / RECEIPT"

if service_type == "Apply Maid New (新女佣申请)":
  total_package_price = 17500.00
  if payment_stage == "Deposit (首付 RM 8,000)":
    doc_title = "DEPOSIT RECEIPT"
    desc_list.append({
        "no": 1,
        "desc": (
            f"Deposit Payment for Maid Recruitment ({maid_name})\n(Part"
            " payment towards total fees)"
        ),
        "price": 8000.00,
        "amount": 8000.00,
    })
    this_payment = 8000.00
    balance_due = 9500.00
    rcpt_no = f"RCP{st.session_state.inv_no[3:]}-1"
  elif payment_stage == "Balance (尾款 RM 9,500)":
    doc_title = "BALANCE RECEIPT"
    desc_list.append({
        "no": 1,
        "desc": (
            f"Balance Payment for Maid ({maid_name})\n(Final settlement)"
        ),
        "price": 9500.00,
        "amount": 9500.00,
    })
    this_payment = 9500.00
    balance_due = 0.00
    rcpt_no = f"RCP{st.session_state.inv_no[3:]}-2"
  else:  # Full Paid
    doc_title = "INVOICE & FULL RECEIPT"
    desc_list = [
        {
            "no": 1,
            "desc": f"Indonesia Maid Recruitment Fee (Maid: {maid_name})",
            "price": 10000.00,
            "amount": 10000.00,
        },
        {
            "no": 2,
            "desc": (
                "Processing, Work Permit, Medical & Documentation Fee"
                f" (Maid: {maid_name})"
            ),
            "price": 7500.00,
            "amount": 7500.00,
        },
    ]
    this_payment = 17500.00
    balance_due = 0.00
    rcpt_no = st.session_state.inv_no
else:
  # 其他一次性服务
  doc_title = "INVOICE / RECEIPT"
  total_package_price = custom_price
  desc_list.append(
      {"no": 1, "desc": f"{service_type}", "price": custom_price, "amount": custom_price}
  )
  this_payment = custom_price
  balance_due = 0.00
  rcpt_no = st.session_state.inv_no

# ================= 渲染打印模板 (Letterhead 样式) =================
st.markdown("---")
st.markdown(
    f"""
<div style="border: 2px solid #333; padding: 20px; font-family: Arial, sans-serif;">
    <!-- Company Letterhead -->
    <div style="text-align: center;">
        <h2 style="margin: 0; color: #1f3bb3;">{COMPANY_INFO['name']}</h2>
        <p style="margin: 2px; font-size: 14px; font-weight: bold;">{COMPANY_INFO['reg_no']}</p>
        <p style="margin: 2px; font-size: 12px;">{COMPANY_INFO['address']}</p>
        <p style="margin: 2px; font-size: 12px;">Email: {COMPANY_INFO['email']} | Tel: {COMPANY_INFO['tel']}</p>
    </div>
    <hr style="border: 1px solid #333; margin: 15px 0;">
    
    <!-- Title & Meta -->
    <table style="width: 100%; font-size: 14px;">
        <tr>
            <td><strong>To:</strong><br>
                <b>{cust_name}</b> (IC NO: {cust_ic})<br>
                {cust_address.replace(chr(10), '<br>')}<br>
                Tel: {cust_tel} | Email: {cust_email}
            </td>
            <td style="text-align: right; vertical-align: top;">
                <h3 style="margin: 0; color: #d9534f;">{doc_title}</h3>
                <p style="margin: 4px 0;"><b>NO/RCPT NO:</b> {rcpt_no}</p>
                <p style="margin: 4px 0;"><b>ISSUE DATE:</b> {issue_date}</p>
            </td>
        </tr>
    </table>
    <br>
    
    <!-- Items Table -->
    <table style="width: 100%; border-collapse: collapse; font-size: 14px;" border="1">
        <thead>
            <tr style="background-color: #f2f2f2;">
                <th style="padding: 8px; width: 10%; text-align: center;">NO</th>
                <th style="padding: 8px; width: 60%; text-align: left;">DESCRIPTION</th>
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
    
    <!-- Summary section -->
    <div style="float: right; width: 350px; font-size: 14px;">
        <table style="width: 100%; border-collapse: collapse;">
            {f'<tr><td style="padding: 4px;"><b>Total Package Price:</b></td><td style="text-align: right;">RM {total_package_price:,.2f}</td></tr>' if service_type == 'Apply Maid New (新女佣申请)' else ''}
            {f'<tr><td style="padding: 4px;"><b>Previous Paid:</b></td><td style="text-align: right;">RM {8000.00 if payment_stage == "Balance (尾kwan RM 9,500)" else 0.00:,.2f}</td></tr>' if payment_stage == "Balance (尾款 RM 9,500)" else ''}
            <tr><td style="padding: 4px;"><b>This Payment (Paid):</b></td><td style="text-align: right;"><b>RM {this_payment:,.2f}</b></td></tr>
            <tr><td style="padding: 4px; border-top: 1px solid #333;"><b>Balance Due (尾款):</b></td><td style="text-align: right; border-top: 1px solid #333;"><b>RM {balance_due:,.2f}</b></td></tr>
        </table>
    </div>
    <div style="clear: both;"></div>
    
    <br>
    <p style="font-size: 13px; margin: 5px 0;"><b>Pay To / Paid To:</b><br>
    {COMPANY_INFO['name']}<br>
    <b>{COMPANY_INFO['bank']}</b></p>
    
    <div style="text-align: center; margin-top: 20px; font-weight: bold; color: #555;">
        Thank You!
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# 提示保存
st.info(
    "💡 提示：你可以直接在浏览器中使用网页的 **打印功能 (Ctrl+P / Cmd+P)**，并将打印机设置为"
    " **另存为 PDF (Save as PDF)**，即可完美复刻你的收据格式并保存或发送给顾客！"
)
