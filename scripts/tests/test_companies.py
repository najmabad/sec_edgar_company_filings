import pandas as pd


words_count = pd.read_csv("~/ChicagoBooth/Minnis/10_Ks/build/code/sec_edgar_company_filings/scripts/outputs/words_count.csv")


random_sample = words_count.sample(n=10)
random_sample.to_csv("~/ChicagoBooth/Minnis/10_Ks/build/code/sec_edgar_company_filings/scripts/tests/test_companies.csv", index= False)

