import pandas as pd
import numpy as np
from joblib import load

def predict_load(tw=5,a=1000,hw=700,fyw=392,tf=20, bf=225,fyf=355,Ss=200,bl=0,tst=0,bst=0):
    """
    tw: The web thickness (mm)
    a: The web panel length (mm)
    hw: The web height (mm)
    fyw: The web yield strength (MPa)
    tf: The flange thickness (mm)
    bf: The flange width (mm)
    fyf: The flange yield strength (MPa)
    Ss: The loading length (mm)
    bl: The longitudinal stiffener location (mm)
    tst: The width of longitudinal stiffener (mm)
    bst: The thickness of longitudinal stiffener (mm)
    """
    input = [[tw,a,hw,fyw,tf,bf,fyf,Ss,bl,tst,bst]]
    input = pd.DataFrame(input)
    scale_stiff = [6, 3000, 1274, 483, 40, 300.5, 485, 690, 327, 30, 110]
    scale_unstiff = [11.8, 3500, 1300, 458, 84.5, 355, 427, 1448, 1, 1, 1]
    y_stiff = 778
    y_unstiff = 888
    if bl == 0 and tst == 0 and bst==0:
        X_test = input.copy()
        for col, divisor in zip(input.columns, scale_unstiff):
            X_test[col] = input[col] / divisor
        result = []
        for num_model in range(1,20,1):
            model = load(f'xgb_unstiff_{num_model}')
            result.append(model.predict(X_test)*y_unstiff)
    else:
        X_test = input.copy()
        for col, divisor in zip(input.columns, scale_stiff):
            X_test[col] = input[col] / divisor
        result = []
        for num_model in range(1, 20, 1):
            model = load(f'xgb_stiff_{num_model}')
            result.append(model.predict(X_test) * y_stiff)
    return np.mean(result)




