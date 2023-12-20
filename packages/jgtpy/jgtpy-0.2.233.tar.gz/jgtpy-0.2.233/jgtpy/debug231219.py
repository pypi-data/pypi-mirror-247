
# %% import
import JGTPDSP as pds
import JGTIDS as ids


# %%  pds
p=pds.getPH("EUR/USD","H4")

# %% ohlc

o=pds.read_ohlc_df_from_file("../data/pds/EUR-USD_H1.csv")


# %%
