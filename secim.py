# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np

# Veriyi oku
df = pd.read_csv(r"C:\Users\Lenovo\Desktop\genel25_26_referandum2017_27meclis_cb2018.csv")


# NUTS1 kodunu oluştur
df["province.NUTS1"] = df["province.NUTS3"].astype(str).str[:3]

# İstenmeyen sütunları filtrele (Haziran, 2018cb, referandum, EVET, HAYIR)
pattern = r"(Haziran|2018cb|referandum|EVET|HAYIR)"
df = df.loc[:, ~df.columns.str.contains(pattern)]

# Katılmayan seçmen (abstain) sütunlarını hesapla
df["ABS.Kasim"] = df["voter.count.Kasim"] - (
    df["total.valid.vote.count.Kasim"] + df["invalid.vote.count.Kasim"]
)
df["ABS.2018meclis"] = df["voter.count.2018meclis"] - df["voted.count.2018meclis"]

# Satır (2015 Kasım) ve sütun (2018 Meclis) partileri
row_parties = [
    "AKP.Kasim", "CHP.Kasim", "HDP.Kasim", "MHP.Kasim",
    "ABS.Kasim", "invalid.vote.count.Kasim"
]
col_parties = [
    "AKP.2018meclis", "CHP.2018meclis", "MHP.2018meclis",
    "HDP.2018meclis", "IYI.2018meclis", "ABS.2018meclis",
    "invalid.vote.count.2018meclis"
]

# Toplam seçmen sayıları (normalize etmek için)
row_totals = df["voter.count.Kasim"]
col_totals = df["voter.count.2018meclis"]

# Geçiş matrisini başlat
transition_matrix = np.zeros((len(row_parties), len(col_parties)))

# Basit ortalama oranlara göre geçiş matrisi oluştur
for i, row_party in enumerate(row_parties):
    for j, col_party in enumerate(col_parties):
        oranlar = (df[row_party] / row_totals) * (df[col_party] / col_totals)
        transition_matrix[i][j] = oranlar.mean()

# Sonucu bir DataFrame olarak yazdır
transition_df = pd.DataFrame(
    transition_matrix, index=row_parties, columns=col_parties
)

print("\n--- Oy Geçiş Matrisi (Ortalama Tahmini) ---\n")
print(transition_df.round(4))