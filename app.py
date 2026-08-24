import datetime
import streamlit as st

st.set_page_config(
    page_title="Agensi Pekerjaan Reliance Maid - 智能开单系统",
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

# 侧边栏：客户资料
st.sidebar.header("1. 客户资料")
cust_name = st.sidebar.text_input("客户姓名", "GAN JUN HENG")
cust_ic = st.sidebar.text_input("身份证/护照号 (IC NO)", "")
cust_address = st.sidebar.text_area(
    "地址", "NO 79, JALAN NAKHODA 14, TAMAN UNGKU TUN AMINAH, 81300 SKUDAI, JOHOR."
)
cust_tel = st.sidebar.text_input("电话", "010-663 5030")

st.sidebar.markdown("---")
st.sidebar.header("2. 单据类型 (智能联动)")
doc_title = st.sidebar.selectbox(
    "单据类型",
    [
        "INVOICE",
        "RECEIPT DEPOSIT",
        "RECEIPT BALANCE",
        "INVOICE / RECEIPT",
    ],
)
rcpt_no = st.sidebar.text_input(
    "单据编号 (No)",
    (
        "INV00004"
        if doc_title == "INVOICE"
        else "RCP00004-1" if "DEPOSIT" in doc_title else "RCP00004-2"
    ),
)
issue_date = st.sidebar.date_input("单据日期", datetime.date.today())

st.sidebar.markdown("---")
st.sidebar.header("3. 核心总价设定")
total_pkg = st.sidebar.number_input("Total Package Price (总套餐价)", value=17500.0)

# 默认定金金额（你可以随时在这里改，或者系统根据选项自动给建议）
default_deposit = 8000.0

items = []
current_amount = 0.0

# 🌟 关键：根据你选择的单据类型，系统自动生成对应的描述和金额！
if doc_title == "INVOICE":
  # Invoice 显示两个大项
  items = [
      {
          "no": 1,
          "desc": "Indonesia Maid Recruitment Fee\n(Maid: Sri Haryati)",
          "amount": 10000.0,
      },
      {
          "no": 2,
          "desc": (
              "Processing, Work Permit, Medical & Documentation Fee\n(Maid:"
              " Sri Haryati)"
          ),
          "amount": 7500.0,
      },
  ]
  current_amount = total_pkg
  previous_paid = 0.0
  balance_due = 0.0
  is_paid_full = False

elif doc_title == "RECEIPT DEPOSIT":
  # 定金收据
  deposit_amt = st.sidebar.number_input(
      "本次收取的定金金额 (Deposit)", value=default_deposit
  )
  items = [{
      "no": 1,
      "desc": (
          f"Deposit Payment for Maid Recruitment (Sri Haryati)\n(Part payment"
          f" towards total fees)"
      ),
      "amount": deposit_amt,
  }]
  current_amount = deposit_amt
  previous_paid = 0.0
  balance_due = total_pkg - current_amount
  is_paid_full = False

elif doc_title == "RECEIPT BALANCE":
  # 尾款收据：自动计算剩余尾款！
  prev_paid = st.sidebar.number_input(
      "之前已付的定金 (Previous Deposit)", value=default_deposit
  )
  auto_balance = max(0.0, total_pkg - prev_paid)
  balance_amt = st.sidebar.number_input(
      "本次收取的尾款金额 (Balance)", value=auto_balance
  )
  items = [{
      "no": 1,
      "desc": (
          f"Balance Payment for Maid (Sri Haryati)\n(Final settlement)"
      ),
      "amount": balance_amt,
  }]
  current_amount = balance_amt
  previous_paid = prev_paid
  balance_due = max(0.0, total_pkg - (previous_paid + current_amount))
  is_paid_full = balance_due == 0.0

else:
  # INVOICE / RECEIPT 一次性付清
  items = [{
      "no": 1,
      "desc": "Full Payment for Maid Recruitment Package (Sri Haryati)",
      "amount": total_pkg,
  }]
  current_amount = total_pkg
  previous_paid = 0.0
  balance_due = 0.0
  is_paid_full = True

# 拼装表格行 HTML
rows_html = ""
for item in items:
  rows_html += f"""
    <tr>
        <td style="padding: 10px; text-align: center; border: 1px solid #333; width: 10%;">{item['no']}</td>
        <td style="padding: 10px; border: 1px solid #333; width: 55%; white-space: pre-line;">{item['desc']}</td>
        <td style="padding: 10px; text-align: right; border: 1px solid #333; width: 17%;">RM {item['amount']:,.2f}</td>
        <td style="padding: 10px; text-align: right; border: 1px solid #333; width: 18%;">RM {item['amount']:,.2f}</td>
    </tr>
    """

# 摘要部分 HTML：完美对齐你给的 PDF 格式
if doc_title == "INVOICE":
  summary_html = f"""
    <h3 style="text-align: right; margin-top: 15px;">Total Amount: RM {current_amount:,.2f}</h3>
    """
elif doc_title == "RECEIPT DEPOSIT":
  summary_html = f"""
    <div style="float: right; width: 360px; margin-top: 15px; font-size: 14px;">
        <table style="width: 100%; border-collapse: collapse;">
            <tr><td style="padding: 5px;"><b>Total Package Price:</b></td><td style="text-align: right; padding: 5px;">RM {total_pkg:,.2f}</td></tr>
            <tr><td style="padding: 5px;"><b>This Payment (Paid):</b></td><td style="text-align: right; padding: 5px;"><b>RM {current_amount:,.2f}</b></td></tr>
            <tr><td style="padding: 5px; border-top: 1px solid #333;"><b>Balance Due (尾款):</b></td><td style="text-align: right; padding: 5px; border-top: 1px solid #333;"><b>RM {balance_due:,.2f}</b></td></tr>
        </table>
    </div>
    <div style="clear: both;"></div>
    """
elif doc_title == "RECEIPT BALANCE":
  summary_html = f"""
    <div style="float: right; width: 380px; margin-top: 15px; font-size: 14px;">
        <table style="width: 100%; border-collapse: collapse;">
            <tr><td style="padding: 5px;"><b>Total Package Price:</b></td><td style="text-align: right; padding: 5px;">RM {total_pkg:,.2f}</td></tr>
            <tr><td style="padding: 5px;"><b>Previous Paid (Deposit):</b></td><td style="text-align: right; padding: 5px;">RM {previous_paid:,.2f}</td></tr>
            <tr><td style="padding: 5px;"><b>This Payment (Paid):</b></td><td style="text-align: right; padding: 5px;"><b>RM {current_amount:,.2f}</b></td></tr>
            <tr><td style="padding: 5px; border-top: 1px solid #333;"><b>Balance Due:</b></td><td style="text-align: right; padding: 5px; border-top: 1px solid #333;"><b>RM {balance_due:,.2f} {"(PAID IN FULL)" if is_paid_full else ""}</b></td></tr>
        </table>
    </div>
    <div style="clear: both;"></div>
    """
else:
  summary_html = f"""
    <h3 style="text-align: right; margin-top: 15px;">Total Amount Paid: RM {current_amount:,.2f} (PAID IN FULL)</h3>
    """

# 网页排版 HTML
full_invoice_html = f"""
<div style="border: 2px solid #333; padding: 25px; font-family: Arial, sans-serif; background-color: #fff; color: #000;">
    <div style="text-align: center;">
        <h2 style="margin: 0; color: #1f3bb3;">{COMPANY_NAME}</h2>
        <p style="margin: 3px; font-size: 13px; font-weight: bold;">{COMPANY_REG}</p>
        <p style="margin: 3px; font-size: 12px;">{COMPANY_ADDR}</p>
        <p style="margin: 3px; font-size: 12px;">{COMPANY_CONTACT}</p>
    </div>
    <hr style="border: 1px solid #333; margin: 15px 0;">
    
    <table style="width: 100%; font-size: 14px; border:none;">
        <tr style="border:none;">
            <td style="border:none; vertical-align: top; width: 60%;"><strong>To:</strong><br>
                <b>{cust_name}</b><br>
                <b>IC NO:</b> {cust_ic}<br>
                {cust_address}<br>
                Tel: {cust_tel}
            </td>
            <td style="text-align: right; vertical-align: top; border:none; width: 40%;">
                <h3 style="margin: 0; color: #d9534f;">{doc_title}</h3>
                <p style="margin: 4px 0;"><b>INV/RCPT NO:</b> {rcpt_no}</p>
                <p style="margin: 4px 0;"><b>ISSUE DATE:</b> {issue_date}</p>
            </td>
        </tr>
    </table>
    <br>
    
    <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
        <thead>
            <tr style="background-color: #f2f2f2;">
                <th style="padding: 10px; border: 1px solid #333; text-align: center;">NO</th>
                <th style="padding: 10px; border: 1px solid #333; text-align: left;">DESCRIPTION</th>
                <th style="padding: 10px; border: 1px solid #333; text-align: right;">PRICE (RM)</th>
                <th style="padding: 10px; border: 1px solid #333; text-align: right;">AMOUNT (RM)</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
    
    {summary_html}
    
    <br>
    <p style="font-size: 13px; margin-top: 20px;"><b>Pay To / Paid To:</b><br>
    {COMPANY_NAME}<br>
    <b>{COMPANY_BANK}</b></p>
    
    <div style="text-align: center; margin-top: 30px; font-weight: bold; color: #444;">
        Thank You!
    </div>
</div>
"""

st.components.v1.html(full_invoice_html, height=750, scrolling=True)

st.markdown("---")
st.info(
    "💡 **如何下载 PDF？**\n\n"
    "点击手机浏览器右上角菜单（三个点 **`...`**），选择 **`分享`** 或 **`打印`**，"
    "再选择 **`另存为 PDF`** 即可完美下载对应的发票或收据！"
)
