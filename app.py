import datetime
import pdfkit
from pyhtml2pdf import *
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

# 侧边栏：自由输入客户资料
st.sidebar.header("1. 客户资料 (可随时修改)")
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

# 让用户自由添加多行项目
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

# 拼装 HTML 表格行
rows_html = ""
for item in items:
  rows_html += f"""
    <tr>
        <td style="padding: 8px; text-align: center; border: 1px solid #333;">{item['no']}</td>
        <td style="padding: 8px; border: 1px solid #333;">{item['desc']}</td>
        <td style="padding: 8px; text-align: right; border: 1px solid #333;">RM {item['amount']:,.2f}</td>
    </tr>
    """

# 网页端实时预览
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

col1, col2 = st.columns([1.2, 0.8])
with col1:
  st.markdown("**To:**")
  st.markdown(f"**{cust_name}**")
  if cust_ic:
    st.markdown(f"**IC NO:** {cust_ic}")
  st.markdown(f"{cust_address}")
  st.markdown(f"Tel: {cust_tel}")

with col2:
  st.markdown(
      f"### <span style='color:red;'>{doc_title}</span>",
      unsafe_allow_html=True,
  )
  st.markdown(f"**No:** {rcpt_no}")
  st.markdown(f"**Date:** {issue_date}")

st.markdown("---")
st.markdown("#### 费用明细 (Description)")

# 用原生的表格展示预览
for item in items:
  c1, c2, c3 = st.columns([0.1, 0.7, 0.2])
  c1.write(str(item["no"]))
  c2.write(item["desc"])
  c3.write(f"RM {item['amount']:,.2f}")

st.markdown("---")
st.success(f"### 总计 (Total): RM {total_amount:,.2f}")

st.markdown(
    f"**Pay To / Paid To:**\n\n{COMPANY_NAME}\n\n**{COMPANY_BANK}**",
    unsafe_allow_html=True,
)
st.markdown(
    "<h4 style='text-align: center; color: gray;'>Thank You!</h4>",
    unsafe_allow_html=True,
)

# 生成完整标准 PDF 的 HTML 模版
pdf_html = f"""
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: Arial, sans-serif; padding: 20px; color: #000;">
    <div style="text-align: center;">
        <h2 style="margin: 0; color: #1f3bb3;">{COMPANY_NAME}</h2>
        <p style="margin: 2px; font-size: 13px; font-weight: bold;">{COMPANY_REG}</p>
        <p style="margin: 2px; font-size: 12px;">{COMPANY_ADDR}</p>
        <p style="margin: 2px; font-size: 12px;">{COMPANY_CONTACT}</p>
    </div>
    <hr style="border: 1px solid #333; margin: 15px 0;">
    
    <table style="width: 100%; font-size: 14px; border:none;">
        <tr>
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
    
    <br><br>
    <p style="font-size: 13px;"><b>Pay To / Paid To:</b><br>
    {COMPANY_NAME}<br>
    <b>{COMPANY_BANK}</b></p>
    
    <div style="text-align: center; margin-top: 40px; font-weight: bold; color: #444;">
        Thank You!
    </div>
</body>
</html>
"""

# 下载 PDF 按钮逻辑
st.markdown("---")
if st.button("📥 点击生成并下载 PDF 收据"):
  try:
    # 临时保存为 HTML 然后转 PDF
    with open("temp_receipt.html", "w", encoding="utf-8") as f:
      f.write(pdf_html)

    # 尝试转换
    pdfkit.from_file("temp_receipt.html", "output.pdf")

    with open("output.pdf", "rb") as pdf_file:
      st.download_button(
          label="👉 点击这里保存 PDF 文件到手机",
          data=pdf_file,
          file_name=f"{rcpt_no}_{cust_name}.pdf",
          mime="application/pdf",
      )
    st.success("PDF 生成成功，请点击上方按钮下载！")
  except Exception as e:
    st.info(
        "提示：由于云端服务器限制，如果直接下载 PDF 遇到环境报错，您也可以直接在手机浏览器上"
        "使用网页的 **分享 / 打印 (Print to PDF)** 功能直接把当前页面保存为完美 PDF！"
    )
