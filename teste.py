import psycopg2

try:
    conn = psycopg2.connect("postgresql://lista_tst_user:Q6l0XHfKeqCKdNz5kEnPv88zrYqfSYLN@dpg-d0edlsuuk2gs73fcp5a0-a/lista_tst")
    print("Conectado com sucesso!")
    conn.close()
except Exception as e:
    print("Erro:", e)
