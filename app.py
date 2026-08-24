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
cust_ic = st.sidebar.text_input("身份证/护照号 (IC NO)", "960226-01-6725")
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

# 生成精美单据预览
rows_html = ""
for item in items:
  rows_html += f"""
    <tr>
        <td style="padding: 8px; text-align: center; border: 1px solid #333;">{item['no']}</td>
        <td style="padding: 8px; border: 1px solid #333;">{item['desc']}</td>
        <td style="padding: 8px; text-align: right; border: 1px solid #333;">RM {item['amount']:,.2f}</td>
    </tr>
    """

invoice_html = f"""
<div style="border: 2px solid #333; padding: 25px; font-family: Arial, sans-serif; background-color: #fff; color: #000;">
    <div style="text-align: center;">
        <h2 style="margin: 0; color: #1f3bb3;">{COMPANY_NAME}</h2>
        <p style="margin: 2px; font-size: 13px; font-weight: bold;">{COMPANY_REG}</p>
        <p style="margin: 2px; font-size: 12px;">{COMPANY_ADDR}</p>
        <p style="margin: 2px; font-size: 12px;">{COMPANY_CONTACT}</p>
    </div>
    <hr style="border: 1px solid #333; margin: 15px 0;">
    
    <table style="width: 100%; font-size: 14px; border:none;">
        <tr style="border:none;">
            <td style="border:none; vertical-align: top;"><strong>To:</strong><br>
                <b>{cust_name}</b><br>
                <b>IC NO:</b> {cust_ic}<br>
                {cust_address}<br>
                Tel: {cust_tel}
            </td>
            <td style="text-align: right; vertical-align: top; border:none;">
                <h3 style="margin: 0; color: #d9534f;">{doc_title}</h3>
                <p style="margin: 4px 0;"><b>No:</b> {rcpt_no}</p>
                <p style="margin: 4px 0;"><b>Date:</b> {issue_date}</p>
            </td>
        </tr>
    </table>
    <br>
    
    <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
        <thead>
            <tr style="background-color: #f2f2f2;">
                <th style="padding: 8px; width: 10%; border: 1px solid #333; text-align: center;">NO</th>
                <th style="padding: 8px; width: 65%; border: 1px solid #333; text-align: left;">DESCRIPTION</th>
                <th style="padding: 8px; width: 25%; border: 1px solid #333; text-align: right;">AMOUNT (RM)</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
    
    <h3 style="text-align: right; margin-top: 20px;">Total: RM {total_amount:,.2f}</h3>
    
    <br>
    <p style="font-size: 13px;"><b>Pay To / Paid To:</b><br>
    {COMPANY_NAME}<br>
    <b>{COMPANY_BANK}</b></p>
    
    <div style="text-align: center; margin-top: 30px; font-weight: bold; color: #444;">
        Thank You!
    </div>
</div>
"""

# 在网页上完美呈现收据
st.markdown(invoice_html, unsafe_allow_html=True)

st.markdown("---")
st.info(
    "💡 **如何保存为 PDF？**\n\n"
    "您只需点击手机浏览器右上角的菜单（三个点 **`...`**），选择 **`分享`** 或 **`打印`**，"
    "然后在打印选项里选择 **`另存为 PDF`**（Save as PDF），即可秒速生成并下载完美的 PDF 收据！"
)
