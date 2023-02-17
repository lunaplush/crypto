import yaml
path_yaml_main_params_file="param-main.yml"
with open(path_yaml_main_params_file) as f:
    main_params = yaml.safe_load(f)
data_repository = main_params["path_data"]

#Данные с yahoo finance которые собираются в репозитории
symbols = ["btc-usd", "eth-usd", "ltc-usd", "bnb-usd", "xmr-usd", "atom-usd",
                   "amzn", "tsla", "amd", "nvda", "intc",
           "bmt.de", "tef.mc", "mbg.de"
           ]
symbols_news = ["btc-usd", "eth-usd", "ltc-usd", "bnb-usd", "xmr-usd", "atom-usd"]

#Ключевые слова для поиска в базе новостей
search_keys = {"btc-usd": ["btc", "bitcoin"],
               "eth-usd": ["eth", "ethereum"]
               }
# период в днях, за который строится массив данных с настроениями новостей
days_before = 365