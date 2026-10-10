import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

#解决matplotlib中文乱码
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# =========1.生成模拟陶瓷订单数据=========
np.random.seed(888)
random.seed(888)

total_orders = 8000
categories = ["茶具", "餐具", "花瓶", "雕塑瓷", "装饰摆件"]
provinces = ["江西", "浙江", "广东", "江苏", "上海", "北京", "山东", "福建", "四川", "湖北"]

start = datetime(2025, 1, 1)
data_list = []

for i in range(total_orders):
    order_time = start + timedelta(days=random.randint(0, 364))
    cat = random.choice(categories)
    if cat == "雕塑瓷":
        price = round(np.random.normal(650, 200), 2)
    elif cat == "茶具":
        price = round(np.random.normal(260, 90), 2)
    elif cat == "餐具":
        price = round(np.random.normal(180, 70), 2)
    elif cat == "花瓶":
        price = round(np.random.normal(320, 110), 2)
    else:
        price = round(np.random.normal(220, 80), 2)

    province = random.choice(provinces)
    user_id = np.random.randint(1000, 6000)
    pay_status = 1 if random.random() > 0.07 else 0

    data_list.append({
        "order_id": i+1,
        "user_id": user_id,
        "order_time": order_time,
        "ceramic_category": cat,
        "price": price,
        "province": province,
        "pay_status": pay_status
    })

df = pd.DataFrame(data_list)
df.to_csv("ceramic_shop.csv", index=False, encoding="utf-8-sig")
print("✅原始数据生成完成：ceramic_shop.csv")

# =========2.数据清洗=========
df = pd.read_csv("ceramic_shop.csv", encoding="utf-8-sig")
print("\n数据集形状：", df.shape)
print("\n缺失值统计：")
print(df.isnull().sum())

df["order_time"] = pd.to_datetime(df["order_time"])
df["month"] = df["order_time"].dt.month
df["weekday"] = df["order_time"].dt.weekday

df_pay = df[df["pay_status"] == 1].copy()
df_pay = df_pay[df_pay["price"] > 0]
df_pay = df_pay.drop_duplicates(subset=["order_id"])

print(f"\n清洗前订单总数：{len(df)}")
print(f"清洗后有效支付订单：{len(df_pay)}")

df_pay.to_csv("ceramic_shop_clean.csv", index=False, encoding="utf-8-sig")
print("✅清洗后数据保存完成：ceramic_shop_clean.csv")

# =========3.各维度分析=========
print("\n========【各陶瓷品类销售】========")
cat_analysis = df_pay.groupby("ceramic_category").agg(
    订单量=("order_id", "count"),
    总销售额=("price", "sum"),
    平均客单价=("price", "mean")
).round(2)
print(cat_analysis)

cat_analysis["订单量"].plot(kind="bar", title="各品类订单数量")
plt.show()

print("\n========【省份销售排行】========")
prov_analysis = df_pay.groupby("province").agg(
    订单量=("order_id", "count"),
    总销售额=("price", "sum")
).sort_values("总销售额", ascending=False)
print(prov_analysis)

print("\n========【月度销售趋势】========")
month_analysis = df_pay.groupby("month").agg(
    订单量=("order_id", "count"),
    总销售额=("price", "sum")
)
print(month_analysis)
month_analysis["订单量"].plot(kind="line", marker="o", title="月度订单趋势")
plt.show()

print("\n========【用户复购分析】========")
user_order_cnt = df_pay.groupby("user_id")["order_id"].count().reset_index()
user_order_cnt.columns = ["user_id", "用户下单次数"]

once_buy = len(user_order_cnt[user_order_cnt["用户下单次数"] == 1])
multi_buy = len(user_order_cnt[user_order_cnt["用户下单次数"] >= 2])
total_user = len(user_order_cnt)

print(f"总付费用户数：{total_user}")
print(f"仅下单1次用户：{once_buy}")
print(f"复购用户(>=2次)：{multi_buy}")
print(f"复购率：{multi_buy/total_user:.2%}")
