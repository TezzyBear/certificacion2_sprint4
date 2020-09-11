from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
import numpy as np

class Meassurements:
    def __init__(self, prediccion = None, metrica_1 = None, metrica_2 = None):
        self.prediccion = prediccion
        if(metrica_1 != None):
          self.metrica_1 = round(metrica_1 * 100, 2)        
        if(metrica_2 != None):
          self.metrica_2 = round(metrica_2 * 100, 2)
         
meassurements = Meassurements()

def to_sequences_test(seq_size, obs):
    x = []
    scaler = MinMaxScaler()
    obs = scaler.fit_transform(obs)
    for i in range(len(obs)-seq_size):
        window = obs[i:(i+seq_size)]
        x.append(window) 
    return np.array(x)

def percentage(part, whole): #Funcion para convertir a porcentaje
  return 100 * float(part)/float(whole)

def resultado(truth, lie):   #Funcion para quedarnos con el porcentaje mayor y determinar si es verdad o mentira (o incluso indeterminado pero muy raro que pase)
  if truth > lie:
    return (truth, "Verdad")
  elif lie > truth:
    return (lie, "Mentira")
  else:
    return (truth, "Indeterminado")

def get_prediction(numpyArray, sequenceSize):     
    xPredict = to_sequences_test(sequenceSize, numpyArray) #Resultado del la conversion del numpy array listo para redecir
    modeloLeido = load_model("modelo.h5") #Lectura del modelo de deep learning
    yPredict = modeloLeido.predict(xPredict) #Prediccion de cada una de las filas con el modelo
    yClasses = yPredict.argmax(axis=-1)      #Clase predicha por cada una de las filas (sirve para las funciones de metricas)
    #Inicio - Metrica 1 - Promedio de prediccion por columnas
    metrica_1 = np.mean(yPredict, axis = 0)  #Promedio de la columna verdad (1) y la columna mentira (0) para la metrica 1
    #Fin - Metrica 1
    #Inicio - Metrica 2 - Proporcion directa entre clase
    size = yClasses.size                    #Cantidad de filas
    verdades_1 = np.count_nonzero(yClasses) #Numero de filas predichas como Verdad (1)
    mentiras_0 = size - verdades_1          #Numero de filas predichas como Mentira (0)
    metrica_2 = resultado(verdades_1, mentiras_0) #La variable metrica_2 es una tupla donde el primer elemento es un decimal y el segundo elemento es el resultado (verdad, mentira o indeterminado)
    #Fin - Metrica 2

    #Inicio - Conversion porcentual (Valor que se debe mostrar en la web como resultado)
    metrica_1_porcentual = max(metrica_1) * 100.0
    metrica_2_porcentual = percentage(metrica_2[0], size)
    resultado_prediccion = metrica_2[1]
    #Fin - Conversion porcentual
    #Prints para comprobar resultados (remover en codigo web)

    global meassurements

    meassurements.prediccion = resultado_prediccion
    meassurements.metrica_1 = metrica_1_porcentual
    meassurements.metrica_2 = metrica_2_porcentual

    print("Metrica 1: {:.3f} %".format(metrica_1_porcentual))
    print("Metrica 2: {:.3f} %".format(metrica_2_porcentual))
    print("Prediccion: {}".format(resultado_prediccion))

def getMeassurements():
    global meassurements
    return meassurements