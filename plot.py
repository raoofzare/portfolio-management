from turtle import color
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_curve(file_number, c):
    df = pd.read_excel(f"prediction_{c}_{file_number}.xlsx")

    pred_value = []
    main_value = []
    for i in range(len(df)):
        pred_value.append(df["pred_value"][i])
        main_value.append(df["main_value"][i])
    plt.figure()
    plt.plot(main_value, label= "main_line", color='r')
    plt.plot(pred_value, label= "prediction_line", color='b')
    plt.legend()
    plt.title(f"Dataset{file_number}, c={c}")
    plt.xlabel(f"weeks , error={np.sum((np.array(pred_value)-np.array(main_value))**2)}")
    plt.ylabel("value")
    plt.subplot()


for i in range(1,5):
    for j in [10,15]:
        plot_curve(i,j)

plt.show()
