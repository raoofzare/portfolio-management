import pandas as pd
import gams
import os
import numpy as np

def predict(file_number, c):
    BASE_DIR = os.path.abspath('')
    ws = gams.workspace.GamsWorkspace(working_directory= BASE_DIR)
    db = ws.add_database()
    # main code 
    i_python = [i for i in range(1, 101)]
    t_python = [i for i in range(1, 105)]

    df_IS = pd.read_excel(f'Data\Dataset{file_number}.xlsx', sheet_name='IS_R')
    df_OS = pd.read_excel(f'Data\Dataset{file_number}.xlsx', sheet_name='OS_R')

    i = db.add_set("i", 1)
    for ip in i_python:
        i.add_record(str(ip))

    t = db.add_set("t", 1)
    for tp in t_python:
        t.add_record(str(tp))

    r = db.add_parameter_dc("r", [i, t])
    for ip in i_python:
        for tp in t_python:
            r.add_record((str(ip), str(tp))).value = df_IS.iloc[ip-1][tp]

    rp = db.add_parameter_dc("rp", [t])
    for tp in t_python:
        rp.add_record((str(tp))).value = df_IS.iloc[100][tp]

    opt = ws.add_options()
    opt.defines["gdxincname"] = db.name
    m = ws.add_job_from_file("proj3.gms")
    m.run(opt, databases = db)

    x = np.zeros(100)

    for rec in m.out_db["x"]:
        x[int(rec.key(0)) - 1] = rec.level

    pred_value = []
    main_value = []
    mul_main = 1
    mul_values = np.ones((1,100))
    for j in range(100):
        mul_values[0][j] = x[j]

    for i in range(1,53):
        for j in range(100):
            mul_values[0][j] *= (1 + df_OS.iloc[j][i])
        pred_value.append(np.sum(mul_values))

        mul_main *= (df_OS.iloc[100][i] + 1)
        main_value.append(mul_main)
        

    df_new = pd.DataFrame({'main_value':main_value,
                           'pred_value':pred_value })

    df_new.to_excel(f"prediction_{c}_{file_number}.xlsx")  

predict(1.15)
predict(2,15)
predict(3,15)
predict(4,15)
